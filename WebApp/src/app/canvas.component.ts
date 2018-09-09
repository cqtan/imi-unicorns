// Angular dependencies
import { Component, Input, OnChanges, SimpleChanges,  } from '@angular/core';

// Application Services
import { ImageService } from './services/image.service';
import { ModalService } from './services/modal.service';

// Application Components
import { ImageModalComponent } from './image-modal.component';

// Data Model Interfaces
import { iImage } from './models/image.model';
import { Category } from './models/category.model';
import { StabiCategory } from './models/stabi-category.model';
import { ColorCategory } from './models/color-category.model';


@Component({
    selector: 'canvas-component',
    styleUrls: ['stylesheets/css/main.css'],
    templateUrl: './templates/canvas.component.html'
})

export class CanvasComponent implements OnChanges {
    // variables to keep track of the given category, genre, color specs and active ppns filtered by range
    @Input() category: Category;
    @Input() stabiCategory: StabiCategory;
    @Input() color: ColorCategory;
    @Input() activePPNs: any;

    // thumbnail height and width replace by actual thumbnails to reduce processing load
    imageHeight: number = 200;
    imageWidth: number;

    // original image set for given property
    images: iImage[];
    // image set after filtering with the current active ppns array
    filteredImages: iImage[];

    // current zoom ratio
    @Input() zoomFactor: number;

    // id and current page number of the pagination component
    id: number;
    pageNumber: number;

    constructor(private imageService: ImageService, private modalService: ModalService) {
        this.id = Math.floor(Math.random() * 1000) + 1;
    }

    // listens to angular based change events
    ngOnChanges(changes: SimpleChanges) {
        // only react on category changes
        if (changes['category']) {
            if (this.category) {
                this.images = null;
                this.setImagesForCategory();
                this.pageNumber = 1;
            }
        }

        // only react on stabi category changes
        if (changes['stabiCategory']) {
            if (this.stabiCategory) {
                this.images = null;
                this.setImagesForStabiCategory();
                this.pageNumber = 1;
            }
        }

        // only reactn on color category changes
        if (changes['color']) {
            if (this.color) {
                this.images = null;
                this.setImagesForColor();
                this.pageNumber = 1;
            }
        }

        //this.intialFilter();
    }

    // calculate the width of the thumbnails (temporary measures to create thumbnails)
    public calculateWidth(image: HTMLImageElement) {
        return (this.imageHeight / image.height) * (image.width * this.zoomFactor)
    }

    // open the image modal when clicked on an image
    public openImageModal(imagesSrc: iImage) {
        this.modalService.init(ImageModalComponent, { image: imagesSrc }, {});
    }

    // destroy the image modal created by this component when called
    public destroyModal() {
        this.modalService.destroy();
    }

    // set the images array for the chosen category
    setImagesForCategory() {
        this.imageService.getImageForFeature(this.category.feature)
            .subscribe((response: iImage[]) => {
                this.images = response;
                this.intialFilter();
            });
    }

    // set the images array for the chosen stabi category
    setImagesForStabiCategory() {
        this.imageService.getImageForSubject(this.stabiCategory.name)
            .subscribe((response: iImage[]) => {
                this.images = response;
                this.intialFilter();
            })
    }

    // set the images array for the chosen color category
    setImagesForColor() {
        this.imageService.getImageForColor(this.color.name)
            .subscribe((response: iImage[]) => {
                this.images = response;
                this.intialFilter();
            })
    }

    // filter the images accoding to the active books
    intialFilter() {
        if (this.images) {
            if (!this.images) return;
            if (!this.activePPNs) return this.images;
            this.filteredImages = this.images.filter(
                (el: any) => {
                    for (let i = 0; i < this.activePPNs.length; i++) {
                        if (el.ppn.indexOf(this.activePPNs[i].identifier) != -1) {
                            return true;
                        }
                    }
                    return false;
                })
        }
    }
}

