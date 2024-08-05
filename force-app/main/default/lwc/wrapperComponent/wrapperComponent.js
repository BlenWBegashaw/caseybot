// import { LightningElement, wire } from 'lwc';
// import { publish, MessageContext } from 'lightning/messageService';
// import SAMPLEMC from '@salesforce/messageChannel/SampleMessageChannel__c';
// import { getRecord } from 'lightning/uiRecordApi';
// import CASE_SUBJECT_FIELD from '@salesforce/schema/Case.Subject';
// import CASE_DESCRIPTION_FIELD from '@salesforce/schema/Case.Description';

// const FIELDS = [CASE_SUBJECT_FIELD, CASE_DESCRIPTION_FIELD];

// export default class WrapperComponent extends LightningElement {
//     @wire(MessageContext)
//     messageContext;

//     @api recordId;
//     caseSubject;
//     caseDescription;

//     @wire(getRecord, { recordId: '$recordId', fields: FIELDS })
//     case({ error, data }) {
//         if (data) {
//             this.caseSubject = data.fields.Subject.value;
//             this.caseDescription = data.fields.Description.value;
//             this.publishCaseDetails();
//         } else if (error) {
//             console.error(error);
//         }
//     }

//     publishCaseDetails() {
//         const message = {
//             subject: this.caseSubject,
//             description: this.caseDescription
//         };
//         publish(this.messageContext, SAMPLEMC, message);
//     }
// }

