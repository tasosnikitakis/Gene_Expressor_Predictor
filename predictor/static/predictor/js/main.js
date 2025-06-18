document.addEventListener('DOMContentLoaded', function () {

    // --- CHART.JS SETUP ---
    const ctx = document.getElementById('pcaChart').getContext('2d');
    const pcaChartElement = document.getElementById('pcaChart');
    const chartLoadingIndicator = document.getElementById('loading-chart');
    let pcaChart; // To hold the chart instance

    // Define a color map for the different cancer types for consistent coloring
    const cancerColorMap = {
        'BRCA': 'rgba(255, 99, 132, 0.7)',  // Red
        'KIRC': 'rgba(54, 162, 235, 0.7)',  // Blue
        'LUAD': 'rgba(255, 206, 86, 0.7)',  // Yellow
        'PRAD': 'rgba(75, 192, 192, 0.7)',  // Green
        'COAD': 'rgba(153, 102, 255, 0.7)' // Purple
    };

    /**
     * Fetches PCA data from the backend API and renders the scatter plot.
     */
    async function fetchAndRenderChart() {
        try {
            const response = await fetch('/predictor/get_pca_data/');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const data = await response.json();

            // Hide loading indicator and show the chart canvas
            chartLoadingIndicator.style.display = 'none';
            pcaChartElement.style.display = 'block';

            // Prepare data for Chart.js
            const datasets = Object.keys(cancerColorMap).map(cancerType => {
                return {
                    label: cancerType,
                    data: data.filter(d => d.Class === cancerType).map(d => ({ x: d.PC1, y: d.PC2 })),
                    backgroundColor: cancerColorMap[cancerType],
                    borderColor: cancerColorMap[cancerType].replace('0.7', '1'),
                    pointRadius: 5,
                    pointHoverRadius: 8
                };
            });
            
            // Create the chart
            pcaChart = new Chart(ctx, {
                type: 'scatter',
                data: {
                    datasets: datasets
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            title: {
                                display: true,
                                text: 'Principal Component 1'
                            }
                        },
                        y: {
                            title: {
                                display: true,
                                text: 'Principal Component 2'
                            }
                        }
                    },
                    plugins: {
                        legend: {
                            position: 'top',
                        },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return `${context.dataset.label}: (PC1: ${context.raw.x.toFixed(2)}, PC2: ${context.raw.y.toFixed(2)})`;
                                }
                            }
                        }
                    }
                }
            });

        } catch (error) {
            console.error('Error fetching PCA data:', error);
            chartLoadingIndicator.textContent = 'Failed to load chart data.';
        }
    }

    // --- PREDICTION LOGIC ---
    const predictButton = document.getElementById('predict-button');
    const predictionResultDiv = document.getElementById('prediction-result');
    const resultContainer = document.getElementById('result-content');
    const predictionLoadingIndicator = document.getElementById('loading-prediction');

    // Result display elements
    const sampleNameEl = document.getElementById('sample-name');
    const predictedClassEl = document.getElementById('predicted-class');
    const trueClassEl = document.getElementById('true-class');
    const resultMatchEl = document.getElementById('result-match');

    /**
     * Fetches a prediction from the backend and updates the UI.
     */
    async function getPrediction() {
        // Show loading state
        predictionResultDiv.style.display = 'block';
        resultContainer.style.display = 'none';
        predictionLoadingIndicator.style.display = 'block';
        
        try {
            const response = await fetch('/predictor/predict/');
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const result = await response.json();
            
            // Update the UI with the results
            sampleNameEl.textContent = result.sample_name;
            
            predictedClassEl.textContent = result.predicted_class;
            predictedClassEl.style.backgroundColor = cancerColorMap[result.predicted_class];

            trueClassEl.textContent = result.true_class;
            trueClassEl.style.backgroundColor = cancerColorMap[result.true_class];
            
            // Check if the prediction was correct
            if (result.predicted_class === result.true_class) {
                resultMatchEl.textContent = "✔ Correct Prediction";
                resultMatchEl.className = 'match';
            } else {
                resultMatchEl.textContent = "❌ Incorrect Prediction";
                resultMatchEl.className = 'mismatch';
            }

        } catch (error) {
            console.error('Error fetching prediction:', error);
            resultContainer.innerHTML = '<p style="color: red;">Failed to get prediction.</p>';
        } finally {
            // Hide loading state and show results
            predictionLoadingIndicator.style.display = 'none';
            resultContainer.style.display = 'block';
        }
    }

    // Attach event listener to the button
    predictButton.addEventListener('click', getPrediction);

    // Initial chart render when the page loads
    fetchAndRenderChart();
});
