document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('routeForm');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');

    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();

            const startCity = document.getElementById('start_city').value;
            const endCity = document.getElementById('end_city').value;

            // Clear previous results
            errorDiv.innerHTML = '';
            resultDiv.innerHTML = '';

            // Validate selections
            if (!startCity || !endCity) {
                showError('Please select both start and end cities.');
                return;
            }

            if (startCity === endCity) {
                showError('Start and end cities must be different.');
                return;
            }

            // Show loading
            loadingDiv.classList.add('active');

            try {
                const response = await fetch('/api/routes', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        start_city: startCity,
                        end_city: endCity
                    })
                });

                const data = await response.json();
                loadingDiv.classList.remove('active');

                if (data.error) {
                    showError(data.error);
                } else if (data.all_paths && data.all_paths.length > 0) {
                    displayResults(data);
                } else {
                    showError('No routes found between these cities.');
                }
            } catch (error) {
                loadingDiv.classList.remove('active');
                showError('An error occurred: ' + error.message);
            }
        });
    }

    function showError(message) {
        errorDiv.innerHTML = `<div class="error">${message}</div>`;
    }

    function displayResults(data) {
        let html = '<div class="result"><h3>Routes Found:</h3>';

        data.all_paths.forEach((path, index) => {
            const badgeClass = path.est_optimal ? 'optimal' : 'alternative';
            const badgeText = path.est_optimal ? '⭐ Optimal' : `Alternative ${index}`;

            html += `
                <div class="path-card path-${index + 1}">
                    <div class="path-header">
                        <span class="badge ${badgeClass}">${badgeText}</span>
                        <strong>Route ${index + 1}</strong>
                    </div>
                    <div class="path-info">
                        <p><strong>Route:</strong> ${path.route_str}</p>
                        <p><strong>Distance:</strong> ${path.distance} km
            `;

            if (!path.est_optimal) {
                html += `<span class="difference">(+${path.difference} km, +${path.pourcentage.toFixed(1)}%)</span>`;
            }

            html += `</p></div></div>`;
        });

        if (data.image_data) {
            html += `
                <hr>
                <h4>Route Visualization:</h4>
                <img src="data:image/png;base64,${data.image_data}" alt="Route graph" style="width: 100%; height: auto; border: 1px solid #ccc;">
            `;
        }

        html += '</div>';
        resultDiv.innerHTML = html;
    }
});
