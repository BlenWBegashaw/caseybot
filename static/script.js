// document.addEventListener('DOMContentLoaded', (event) => {
//     fetchRecommendations();
// });

// function fetchRecommendations() {
//     fetch('/match_cases', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             case: {
//                 subject: 'Automatically fetched subject',
//                 description: 'Automatically fetched description'
//             }
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         displayRecommendations(data);
//     })
//     .catch(error => {
//         console.error('Error fetching recommendations:', error);
//     });
// }

// function displayRecommendations(recommendations) {
//     const recommendationsContainer = document.getElementById("recommendations");
//     recommendationsContainer.innerHTML = '';

//     if (recommendations.length > 0) {
//         const list = document.createElement('ul');
//         recommendations.forEach(rec => {
//             const listItem = document.createElement('li');
//             listItem.innerHTML = `
//                 <a href="${rec.case_link}" target="_blank">${rec.subject}</a>
//                 <p>${rec.description}</p>
//                 <p>Similarity: ${rec.similarity}</p>
//             `;
//             list.appendChild(listItem);
//         });
//         recommendationsContainer.appendChild(list);
//     } else {
//         recommendationsContainer.innerHTML = '<p>No recommendations found.</p>';
//     }
// }

document.addEventListener('DOMContentLoaded', (event) => {
    fetchRecommendations();
});

// function fetchRecommendations() {
//     const currentUrl = window.location.href; // Get the current URL

//     fetch('/match_cases', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             case: {
//                 url: currentUrl // Include the current URL in the payload
//             }
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         displayRecommendations(data);
//     })
//     .catch(error => {
//         console.error('Error fetching recommendations:', error);
//     });
// }

// function displayRecommendations(recommendations) {
//     const recommendationsContainer = document.getElementById("recommendations");
//     recommendationsContainer.innerHTML = '';

//     if (recommendations.length > 0) {
//         const list = document.createElement('ul');
//         recommendations.forEach(rec => {
//             const listItem = document.createElement('li');
//             listItem.innerHTML = `
//                 <a href="${rec.case_link}" target="_blank">${rec.subject}</a>
//                 <p>${rec.description}</p>
//                 <p>Similarity: ${rec.similarity}</p>
//             `;
//             list.appendChild(listItem);
//         });
// //         recommendationsContainer.appendChild(list);
// //     } else {
// //         recommendationsContainer.innerHTML = '<p>No recommendations found.</p>';
// //     }
// // }
// document.addEventListener('DOMContentLoaded', (event) => {
//     fetchRecommendations();
// });

// function fetchRecommendations() {
//     const currentUrl = window.location.href; // Get the current URL

//     fetch('/match_cases', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json'
//         },
//         body: JSON.stringify({
//             case: {
//                 url: currentUrl // Include the current URL in the payload
//             }
//         })
//     })
//     .then(response => response.json())
//     .then(data => {
//         displayRecommendations(data);
//     })
//     .catch(error => {
//         console.error('Error fetching recommendations:', error);
//     });
// }

// function displayRecommendations(recommendations) {
//     const recommendationsContainer = document.getElementById("recommendations");
//     recommendationsContainer.innerHTML = '';

//     if (recommendations.length > 0) {
//         const list = document.createElement('ul');
//         recommendations.forEach(rec => {
//             const listItem = document.createElement('li');
//             listItem.innerHTML = `
//                 <a href="${rec.case_link}" target="_blank">${rec.subject}</a>
//                 <p>${rec.description}</p>
//                 <p>Similarity: ${rec.similarity}</p>
//             `;
//             list.appendChild(listItem);
//         });
//         recommendationsContainer.appendChild(list);
//     } else {
//         recommendationsContainer.innerHTML = '<p>No recommendations found.</p>';
//     }
// }
document.addEventListener('DOMContentLoaded', function() {
    // Function to fetch recommendations
    async function fetchRecommendations(caseUrl) {
        try {
            const response = await fetch('/recommend_cases', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ case: { url: caseUrl } })
            });

            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            const data = await response.json();
            displayRecommendations(data);
        } catch (error) {
            console.error('Error fetching recommendations:', error);
        }
    }

    // Function to display recommendations
    function displayRecommendations(recommendations) {
        const recommendationsContainer = document.getElementById('recommendations');
        recommendationsContainer.innerHTML = '';

        recommendations.forEach(rec => {
            const recElement = document.createElement('div');
            recElement.className = 'recommendation';
            recElement.innerHTML = `
                <h3>Case Number: ${rec.case_number}</h3>
                <p>Subject: ${rec.subject}</p>
                <p>Description: ${rec.description}</p>
                <p>Similarity: ${rec.similarity}</p>
                <a href="${rec.case_link}" target="_blank">View Case</a>
            `;
            recommendationsContainer.appendChild(recElement);
        });
    }

    // Example usage: Fetch recommendations for a specific case URL
    const caseUrl = 'https://ciscomeraki4-dev-ed.develop.lightning.force.com/lightning/r/Case/500aj00000FL9RyAAL/view';
    fetchRecommendations(caseUrl);
});
