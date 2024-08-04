import { LightningElement, api, wire } from 'lwc';
import { getRecord } from 'lightning/uiRecordApi';
import CASE_SUBJECT_FIELD from '@salesforce/schema/Case.Subject';
import CASE_DESCRIPTION_FIELD from '@salesforce/schema/Case.Description';

const FIELDS = [CASE_SUBJECT_FIELD, CASE_DESCRIPTION_FIELD];

export default class CaseRecommendationBot extends LightningElement {
    @api recordId;
    caseSubject;
    caseDescription;
    recommendations = [];

    @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
    case({ error, data }) {
        if (data) {
            this.caseSubject = data.fields.Subject.value;
            this.caseDescription = data.fields.Description.value;
            this.fetchRecommendations();
        } else if (error) {
            console.error(error);
        }
    }

    fetchRecommendations() {
        const payload = {
            case: {
                subject: this.caseSubject,
                description: this.caseDescription
            }
        };

        fetch('https://caseybot-3785eca7c1f1.herokuapp.com/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => response.json())
        .then(data => {
            this.recommendations = data;
        })
        .catch(error => {
            console.error('Error fetching recommendations:', error);
        });
    }
}

