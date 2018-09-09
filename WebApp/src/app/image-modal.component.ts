// Angular Dependencies
import { Component, OnInit } from '@angular/core';

// Application Services
import { ModalService } from './services/modal.service';
import { BookService } from "./services/book.service";
import { ImageService } from './services/image.service';

// Application Model Interfaces
import { iImage } from './models/image.model';

import 'leaflet';
import 'leaflet.heat';

declare var L: any;//Declare leaflet lib and plugin

@Component({
    host: {
        '(document:keydown)': 'keyboardInputs($event)'
    },
    selector: 'image-modal',
    styleUrls: ['stylesheets/css/main.css'],
    templateUrl: './templates/image-modal.component.html'
})

/**
 * Component which will implent the modal view of a single image
 */
export class ImageModalComponent implements OnInit {

    public image: iImage;
    public bookInformation: any;
    public stabiLink: string = '';

    private history: any[] = [];
    private siblings: any[];
    private currentIndex = 0;

    constructor(private modalService: ModalService, private bookService: BookService, private imageService: ImageService) {

    }

    ngOnInit() {
        // retrieve initial modal content
        this.getImageData();
        // retrieve the initial siblings of the current book
        this.getSiblings(this.image);
    }

    // pass in a image object to have a clean transition between data 
    changeImage(image: any) {
        // clean up the history the rest of the history if youre adding an image in between
        if(this.currentIndex < (this.history.length - 1)) {
            this.history.splice(this.currentIndex + 1);
        }

        // only add the initial image if you're the first
        if(this.history.length == 0 && this.currentIndex == 0) {
            this.history.push(this.image);
        }

        this.imageService.getImageForObjectID(image[0]._id.$oid).subscribe(result => {
            // increment the global index
            this.currentIndex++;
            // update the current image
            this.image = result[0];
            // update the modal content
            this.getImageData();
            // push the new image into the history
            this.history.push(result[0]);
            // update the siblings array with the content of the new image
            this.getSiblings(result[0]);
        });
    }

    // track the keyboard inputs when this component is active and ignore all default binding
    keyboardInputs(event: KeyboardEvent) {
        event.preventDefault();

        // destroy the current modal and destory the history
        if (event.key === 'Escape') {
            this.history = []; 
            this.modalService.destroy();
        }

        // go back by one element in the current history
        if(event.altKey && event.keyCode === 37) {
            this.iterateBack();
        }

        // go forward by one element in the current history
        if(event.altKey && event.keyCode === 39) {
            this.iterateForward();
        }

        // reload the current active tab (default browser functionality)
        if(event.ctrlKey && event.keyCode === 82) {
            window.location.reload();
        }
    }

    // iterate back in the current active history
    private iterateBack() {
        if(this.currentIndex == 0) {
            return;
        } else {
            this.currentIndex --;
            this.image = this.history[this.currentIndex];
            this.getImageData();
            this.getSiblings(this.image);
        }
    }

    // iterate foward in the current active history
    private iterateForward() {
        if((this.currentIndex == 0 && this.history.length == 0) || this.currentIndex == (this.history.length - 1)) {
            return;
        } else {
            this.currentIndex ++; 
            this.image = this.history[this.currentIndex];
            this.getImageData();
            this.getSiblings(this.image);
        }
    }

    // get the sibilings of the active image
    private getSiblings(image: any) {
        this.siblings = [];
        image.siblings.forEach(sibling => {
            this.imageService.getImageForObjectID(sibling.$oid)
                .subscribe(response => {
                    this.siblings.push(response);
                });
        })
    }

    // method to destroy the modal
    closeModal() {
        this.history = [];
        this.modalService.destroy();
    }

    // initialize the map in the modal
    private initMap(data: any) {
        if (data['latitude'] && data ['longitude']){
            let map = L.map('map').setView([data['latitude'], data ['longitude']], 6);

            let baseLayer =  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoicmFsZSIsImEiOiJjaml0dXpudzcxdnB0M2t0OWg5Z3RxZmN4In0.2FigAU45-61J9pQW2GLH7Q', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
                id: 'mapbox.streets',
            }).addTo(map); 
            let marker = L.marker([data['latitude'], data ['longitude']]).addTo(map);
        }else {
            let map = L.map('map').setView([52.342324, 13.118845], 6);

            let baseLayer =  L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoicmFsZSIsImEiOiJjaml0dXpudzcxdnB0M2t0OWg5Z3RxZmN4In0.2FigAU45-61J9pQW2GLH7Q', {
                attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
                maxZoom: 18,
                id: 'mapbox.streets',
            }).addTo(map); 
        }
    }

    // update all informations in the modal;
    private getImageData() {
        this.bookService.getBookInformationForImage(this.image.ppn)
            .subscribe(data => {
                this.bookInformation = data;
                this.initMap(data);
            });

        this.stabiLink = 'https://digital.staatsbibliothek-berlin.de/werkansicht?PPN=' + this.image.ppn;
    }
}
