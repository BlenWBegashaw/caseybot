import { LightningElement, wire } from 'lwc';
import { publish, MessageContext } from 'lightning/messageService';
import SAMPLEMC from '@salesforce/messageChannel/SampleMessageChannel__c';

export default class WrapperComponent extends LightningElement {
    @wire(MessageContext)
    messageContext;

    handleTextChange(subject, description) {
        const message = {
            subject: subject,
            description: description
        };
        publish(this.messageContext, SAMPLEMC, message);
    }

    renderedCallback() {
        // Use MutationObserver to detect changes in the specific element
        const targetElement = document.querySelector("#brandBand_2 > div > div > div.windowViewMode-normal.oneContent.active.lafPageHost > div > div > one-record-home-flexipage2 > forcegenerated-adg-rollup_component___force-generated__flexipage_-record-page___-case_-record_-page___-case___-v-i-e-w___-l-m-t___1722871855000 > forcegenerated-flexipage_case_record_page_case__view_js___lmt___1722837351000 > record_flexipage-desktop-record-page-decorator > div.record-page-decorator > records-record-layout-event-broker > slot > slot > flexipage-record-home-left-sidebar-template-desktop2 > div > div.slds-col.slds-size_1-of-1.row.region-header > slot > flexipage-component2:nth-child(1) > slot > records-lwc-highlights-panel > records-lwc-record-layout > forcegenerated-highlightspanel_case___012000000000000aaa___compact___view___recordlayout2 > records-highlights2 > div.highlights.slds-clearfix.slds-page-header.slds-page-header_record-home.fixed-position > div.slds-grid.primaryFieldRow > div.slds-grid.slds-col.slds-has-flexi-truncate > div.slds-media__body > h1 > slot > support-output-case-subject-field > div > lightning-formatted-text");
        const descriptionElement = document.querySelector("#brandBand_2 > div > div > div.windowViewMode-normal.oneContent.active.lafPageHost > div > div > one-record-home-flexipage2 > forcegenerated-adg-rollup_component___force-generated__flexipage_-record-page___-case_-record_-page___-case___-v-i-e-w___-l-m-t___1722871855000 > forcegenerated-flexipage_case_record_page_case__view_js___lmt___1722837351000 > record_flexipage-desktop-record-page-decorator > div.record-page-decorator > records-record-layout-event-broker > slot > slot > flexipage-record-home-left-sidebar-template-desktop2 > div > div.slds-col.slds-size_1-of-1.row.region-header > slot > flexipage-component2:nth-child(1) > slot > records-lwc-highlights-panel > records-lwc-record-layout > forcegenerated-highlightspanel_case___012000000000000aaa___compact___view___recordlayout2 > records-highlights2 > div.highlights.slds-clearfix.slds-page-header.slds-page-header_record-home.fixed-position > div.slds-grid.primaryFieldRow > div.slds-grid.slds-col.slds-has-flexi-truncate > div.slds-media__body > p > slot > support-output-case-description-field > div > lightning-formatted-text");

        if (targetElement && descriptionElement) {
            const observer = new MutationObserver((mutationsList) => {
                for (let mutation of mutationsList) {
                    if (mutation.type === 'childList' || mutation.type === 'characterData') {
                        this.handleTextChange(targetElement.innerText, descriptionElement.innerText);
                    }
                }
            });

            observer.observe(targetElement, { childList: true, characterData: true, subtree: true });
            observer.observe(descriptionElement, { childList: true, characterData: true, subtree: true });
        }
    }
}


