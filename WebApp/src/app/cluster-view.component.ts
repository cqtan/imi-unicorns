// Angular Dependencies
import { Component, ComponentFactoryResolver, ComponentRef, ViewChild, ViewContainerRef } from '@angular/core';

// Application Components
import { ClusterRowComponent } from "./cluster-row.component";
import { TimeSliderComponent } from './time-slider.component';


@Component({
    selector: 'cluster-view',
    styleUrls: ['stylesheets/css/main.css'],
    templateUrl: './templates/cluster-view.component.html'
})

/**
 * Component which represents the Cluster-View
 */
export class ClusterView {
    @ViewChild('parent', { read: ViewContainerRef }) container: ViewContainerRef;
    @ViewChild('placeHolder', { read: ViewContainerRef }) timeContainer: ViewContainerRef;

    numberOfRows = 1;
    component: any;
    currentMinMax: number[] = [];
    currentSliderRange: number[];
    zoomFactor: number = 1;

    clusterRow2: ComponentRef<ClusterRowComponent>;
    clusterRow3: ComponentRef<ClusterRowComponent>;

    constructor(private componentFactory: ComponentFactoryResolver) { }

    // creates a new cluster row component
    public insertClusterRow() {
        let factory = this.componentFactory.resolveComponentFactory(ClusterRowComponent);
        let component = this.container.createComponent(factory);
        this.numberOfRows++;
        if(this.numberOfRows == 2) {
            this.zoomFactor = 0.6;
        } else if (this.numberOfRows == 3) {
            this.zoomFactor = 0.4;
        }

        // set component styling cause standart css won't grab here
        component.location.nativeElement.setAttribute('style', 'flex: 1; -webkit-flex: 1; -ms-flex: 1; flex-shrink: 0;');

        // pass in all required inputs of the component
        component.instance._ref = component;
        component.instance.elementNumber = this.numberOfRows;
        component.instance.minMaxRange.subscribe(minMaxRange => this.minMaxOfCategory(minMaxRange));
        component.instance.sliderRange = this.currentSliderRange;
        component.instance.zoomFactor = this.zoomFactor;

        if (!this.clusterRow2 && this.clusterRow2 !== component) {
            this.clusterRow2 = component;
        } else {
            this.clusterRow3 = component;
        }

        // output event of cluster-row
        component.instance.deleted.subscribe(() => this.onDelete());
    }

    // delete event for the created clusters
    onDelete() {
        if (this.numberOfRows == 1) return;
        if( this.numberOfRows == 2) this.zoomFactor = 1;
        if( this.numberOfRows == 3) this.zoomFactor = 0.6;
        this.numberOfRows--;
    }

    // method to change the range of the slider, if the min, max of the new category / stabi category / colour varries
    minMaxOfCategory(event: any) {
        let factory = this.componentFactory.resolveComponentFactory(TimeSliderComponent);

        if (this.currentMinMax.length == 0) {
            this.component = this.timeContainer.createComponent(factory)
            this.currentMinMax[0] = event.min;
            this.currentMinMax[1] = event.max

            let instance = this.component.instance;
            instance.currentMinMax = this.currentMinMax;
            this.currentSliderRange = [this.currentMinMax[0], this.currentMinMax[1]];
            instance.rangeChanged.subscribe(event => this.onRangeChanged(event));

            this.currentSliderRange = [this.currentMinMax[0], this.currentMinMax[1]];
        }

        if (this.currentMinMax.length > 0 && event.min < this.currentMinMax[0]) {
            this.component.destroy();
            this.component = this.timeContainer.createComponent(factory);
            let instance = this.component.instance;

            instance.currentMinMax = this.currentMinMax;
            this.currentSliderRange = [this.currentMinMax[0], this.currentMinMax[1]];
            instance.rangeChanged.subscribe(event => this.onRangeChanged(event));

            this.currentMinMax[0] = event.min;
            this.currentSliderRange = this.currentMinMax;
            if (this.clusterRow2) this.clusterRow2.instance.setSliderRange = this.currentMinMax;
            if (this.clusterRow3) this.clusterRow2.instance.setSliderRange = this.currentMinMax;
        }

        if (this.currentMinMax.length > 0 && event.max > this.currentMinMax[1]) {
            this.component.destroy();
            this.component = this.timeContainer.createComponent(factory);
            let instance = this.component.instance;

            instance.currentMinMax = this.currentMinMax;
            this.currentSliderRange = [this.currentMinMax[0], this.currentMinMax[1]];
            instance.rangeChanged.subscribe(event => this.onRangeChanged(event));

            this.currentMinMax[1] = event.max
            this.currentSliderRange = this.currentMinMax;
            if (this.clusterRow2) this.clusterRow2.instance.setSliderRange = this.currentMinMax;
            if (this.clusterRow3) this.clusterRow3.instance.setSliderRange = this.currentMinMax;
        }
    }

    // event listener for change events on the range of the slider
    onRangeChanged(range: number[]) {
        this.currentSliderRange = range;
        if (this.clusterRow2) this.clusterRow2.instance.setSliderRange = range;
        if (this.clusterRow3) this.clusterRow3.instance.setSliderRange = range;
    }
}
