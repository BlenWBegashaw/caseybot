// import { LightningElement, api, wire } from 'lwc';
// import { subscribe, MessageContext } from 'lightning/messageService';
// import SAMPLEMC from '@salesforce/messageChannel/SampleMessageChannel__c';

// export default class Caseybot extends LightningElement {
//     @api recordId;
//     caseSubject;
//     caseDescription;
//     recommendations = [];
//     showModal = false;
//     subscription = null;

//     @wire(MessageContext)
//     messageContext;

//     connectedCallback() {
//         this.subscribeToMessageChannel();
//     }

//     subscribeToMessageChannel() {
//         if (!this.subscription) {
//             this.subscription = subscribe(
//                 this.messageContext,
//                 SAMPLEMC,
//                 (message) => this.handleMessage(message)
//             );
//         }
//     }

//     handleMessage(message) {
//         this.caseSubject = message.subject;
//         this.caseDescription = message.description;
//     }

//     handleFetchRecommendations() {
//         const payload = {
//             case: {
//                 subject: this.caseSubject,
//                 description: this.caseDescription
//             }
//         };

//         console.log('Payload:', payload); // Log the payload to verify

//         fetch('https://caseybot-3785eca7c1f1.herokuapp.com/match_cases', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(payload)
//         })
//         .then(response => response.json())
//         .then(data => {
//             this.recommendations = data;
//             this.showModal = true;
//             console.log('Recommendations:', this.recommendations);
//         })
//         .catch(error => {
//             console.error('Error fetching recommendations:', error);
//         });
//     }

//     handleCloseModal() {
//         this.showModal = false;
//     }
// }
// import { LightningElement, api, wire } from 'lwc';
// import { getRecord } from 'lightning/uiRecordApi';
// import CASE_SUBJECT_FIELD from '@salesforce/schema/Case.Subject';
// import CASE_DESCRIPTION_FIELD from '@salesforce/schema/Case.Description';

// const FIELDS = [CASE_SUBJECT_FIELD, CASE_DESCRIPTION_FIELD];

// export default class Caseybot extends LightningElement {
//     @api recordId;
//     caseSubject;
//     caseDescription;
//     recommendations = [];
//     showModal = false;

//     @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
//     case({ error, data }) {
//         if (data) {
//             this.caseSubject = data.fields.Subject.value;
//             this.caseDescription = data.fields.Description.value;
//         } else if (error) {
//             console.error(error);
//         }
//     }

//     handleFetchRecommendations() {
//         const currentUrl = window.location.href; // Get the current URL
//         const payload = {
//             case: {
//                 subject: this.caseSubject,
//                 description: this.caseDescription,
//                 url: currentUrl // Include the current URL in the payload
//             }
//         };

//         console.log('Payload:', payload); // Log the payload to verify

//         fetch('https://caseybot-3785eca7c1f1.herokuapp.com/match_cases', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json'
//             },
//             body: JSON.stringify(payload)
//         })
//         .then(response => response.json())
//         .then(data => {
//             this.recommendations = data;
//             this.showModal = true;
//             console.log('Recommendations:', this.recommendations);
//         })
//         .catch(error => {
//             console.error('Error fetching recommendations:', error);
//         });
//     }

//     handleCloseModal() {
//         this.showModal = false;
//     }
// }
import { LightningElement, api, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import CASE_SUBJECT_FIELD from '@salesforce/schema/Case.Subject';
import CASE_DESCRIPTION_FIELD from '@salesforce/schema/Case.Description';

const FIELDS = [CASE_SUBJECT_FIELD, CASE_DESCRIPTION_FIELD];

export default class Caseybot extends LightningElement {
    @api recordId;
    caseSubject;
    caseDescription;
    recommendations = [];
    showModal = false;

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    case({ error, data }) {
        if (data) {
            this.caseSubject = data.fields.Subject.value;
            this.caseDescription = data.fields.Description.value;
        } else if (error) {
            console.error(error);
        }
    }

    handleFetchRecommendations() {
        const currentUrl = window.location.href; // Get the current URL

        fetch('https://your-heroku-app.herokuapp.com/match_cases', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                case: {
                    url: currentUrl // Include the current URL in the payload
                }
            })
        })
        .then(response => response.json())
        .then(data => {
            this.recommendations = data;
            this.showModal = true;
            console.log('Recommendations:', this.recommendations);
        })
        .catch(error => {
            console.error('Error fetching recommendations:', error);
        });
    }

    handleCloseModal() {
        this.showModal = false;
    }
}
