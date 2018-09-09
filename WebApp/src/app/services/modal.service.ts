// Angular Dependencies
import { Injectable, ApplicationRef, OnChanges, EventEmitter } from '@angular/core';

// Application Services
import { DomService } from './dom.service';

/*
 * This service is responsible to create the Modals used in the angular application
 * Reason for using this instead of a simple bootstrap modal is that you have
 * angular2 functionalities when done this way.
 * Clean control of inputs, outputs and event listening in a given modal
 */

@Injectable()
export class ModalService {

    constructor(private domService: DomService, private appRef: ApplicationRef) { }

    private modalElementId = 'modal-container';
    private overlayElementId = 'overlay';

    eventEmitter = new EventEmitter<any>();

    // creates a modal with the component, inputs and outputs passed in
    init(component: any, inputs: any, outputs: any) {
        let componentConfig = {
            inputs: inputs,
            outputs: outputs
        }

        this.domService.appendComponentTo(this.modalElementId, component, componentConfig);
        document.getElementById(this.modalElementId).className = 'show';
        document.getElementById(this.overlayElementId).className = 'show';
    }

    // destroys a created modal
    destroy() {
        this.domService.removeComponent();
        document.getElementById(this.modalElementId).className = 'hidden';
        document.getElementById(this.overlayElementId).className = 'hidden';
    }
}
