function openForm() {
    document.getElementById("myForm").style.display = "block";
}

function closeForm() {
    document.getElementById("myForm").style.display = "none";
}

function fetchRecommendations() {
    const subject = document.getElementById("subject").value;
    const description = document.getElementById("description").value;

    const payload = {
        case: {
            subject: subject,
            description: description
        }
    };

    fetch('/match_cases', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(payload)
    })
    .then(response => response.json())
    .then(data => {
        displayRecommendations(data);
    })
    .catch(error => {
        console.error('Error fetching recommendations:', error);
    });
}

function displayRecommendations(recommendations) {
    const recommendationsContainer = document.getElementById("recommendations");
    recommendationsContainer.innerHTML = '';

    if (recommendations.length > 0) {
        const list = document.createElement('ul');
        recommendations.forEach(rec => {
            const listItem = document.createElement('li');
            listItem.innerHTML = `
                <a href="${rec.case_link}" target="_blank">${rec.subject}</a>
                <p>${rec.description}</p>
                <p>Similarity: ${rec.similarity}</p>
            `;
            list.appendChild(listItem);
        });
        recommendationsContainer.appendChild(list);
    } else {
        recommendationsContainer.innerHTML = '<p>No recommendations found.</p>';
    }
}
