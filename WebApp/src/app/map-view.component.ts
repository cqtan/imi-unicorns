// Angular Dependencies
import { Component, OnInit, OnChanges } from '@angular/core';

// Application Services
import { BookService } from './services/book.service';
import { MapService } from './services/maps.service';

import 'leaflet';
import 'leaflet.heat';
import 'leaflet.markercluster';

declare var L: any; // Declare leaflet lib and plugin

@Component({
    selector: 'map-component',
    styleUrls: ['stylesheets/css/main.css'],
    templateUrl: './templates/map-view.component.html'
})

/**
 * Component which will implement the map view in our application
 */
export class MapView implements OnInit {
    booksInfo: any[];
    minMax: any;
    map: any;
    markers = L.markerClusterGroup({ showCoverageOnHover: true });
    latLongCountData: any[];
    filteredData: any;
    originalData: any[];
    clusterLayer: any;
    heatLayer: any;
    baseLayer: any;
    lightLayer: any;
    layControl: any;

    constructor(private bookService: BookService, private mapService: MapService) { }

    // on initiation create heat and cluster map. Heat map is visible, cluster map shows when choose in the layers control on the right upper corner.
    ngOnInit() {
        // retrieve min max dates of dataset
        this.bookService.getMinMax()
            .subscribe((data: any) => {
                this.minMax = [data.min, data.max];
            });

        // retrieve the lat longs of the data
        this.mapService.getlatLong()
            .then(data => {
                this.latLongCountData = data;
                this.initMap();
                // get latitue and longitute infromation of each book and pass them to create cluster map

                // get the required book informations
                this.bookService.getBooksInformation()
                    .subscribe((data: any) => {
                        this.addNodes(data);
                        this.originalData = data;
                    });
            });
    }
    // get range changes from slider and re-draw the map with the new values
    // creates markers for the cluster map and add them to the layer

    // event listener for the slider
    public onSliderRangeChange(sliderValues: any) {
        this.filterData(sliderValues);
    }

    // add the nodes to the map
    public addNodes(data: any[]) {
        data.forEach(item => {
            const m = L.marker(item.geoData);
            // html sniped to create the content of the markers
            const popup = `
                <div class="container-fluid">
                    <div class="row">
                        <div class="col-12">
                            <h5> Buchtitel </h5>
                        </div>
                        <div class="col-12">
                            <p>` + item.title + `</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12">
                            <h5> Buchautor </h5>
                        </div>
                        <div class="col-12">
                            <p>` + item.creator + `</p>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-12">
                            <a href="https://digital.staatsbibliothek-berlin.de/werkansicht?PPN=` + item.identifier + `" target="_blank"> Zu dem Buch </a>
                        </div
                    </div>
                </div>
            `;
            // bind a popup function to each marker
            m.bindPopup(popup);
            // add them to the map
            this.markers.addLayer(m);
        });
    }
    // on map initiation creates heat and cluster map by creating the layers as global variables

    // initialize the map here
    public initMap() {
        const mapboxUrl = 'https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoicmFsZSIsImEiOiJjaml0dXpudzcxdnB0M2t0OWg5Z3RxZmN4In0.2FigAU45-61J9pQW2GLH7Q';
        const mapboxAttribution = 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>';

        this.baseLayer = L.tileLayer(mapboxUrl, { id: 'mapbox.streets', attribution: mapboxAttribution });
        this.clusterLayer = this.markers;
        this.lightLayer = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/light-v9/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoicmFsZSIsImEiOiJjaml0dXpudzcxdnB0M2t0OWg5Z3RxZmN4In0.2FigAU45-61J9pQW2GLH7Q', { id: 'mapbox.light-v9', attribution: mapboxAttribution });
        this.heatLayer = L.heatLayer(this.latLongCountData,
            {
                minOpacity: 0.2,
                radius: 20,
                blur: 8,
                gradient: { 0.5: 'blue', 0.6: 'lime', 1: 'red', 0.3: 'black' }
            });

        const baseMaps = {
            'Street map': this.baseLayer,
            'Light (grayscale)': this.lightLayer,
        };

        const overlayMaps = {
            'Cluster map': this.clusterLayer,
            'Heat map': this.heatLayer

        };

        this.map = L.map('map', {
            center: [39.73, -104.99],
            zoom: 10,
            layers: [this.baseLayer, this.heatLayer]
        }).setView([51.883549, 12.668406], 6);

        this.layControl = L.control.layers(baseMaps, overlayMaps);
        this.layControl.addTo(this.map);
    }

    public refreshMap() {
        this.map.clusterLayer.clearLayers();
    }

    /* when the time lsider is used. Filters the data, clear and remove the current layers
    * and create new ones in teh global variables, removes and creates new layers control.
    * There was no option to simply update the layers control.
    */

    public filterData(sliderValues: any) {
        if (this.originalData) {
            this.filteredData = this.originalData.filter(
                item => (item.date >= sliderValues[0] && item.date <= sliderValues[1]));
            const heat = [];
            this.filteredData.forEach(item => {
                heat.push(item.geoData);
            });
            this.markers.clearLayers();
            this.addNodes(this.filteredData);
            this.map.removeLayer(this.heatLayer);
            this.heatLayer = L.heatLayer(
                heat,
                {
                    minOpacity: 0.2,
                    radius: 20,
                    blur: 8,
                    gradient: { 0.5: 'blue', 0.6: 'lime', 1: 'red', 0.3: 'black' }
                }).addTo(this.map);
        }
        // creates new layers control , with the new layers
        const baseMaps = {
            'Street map': this.baseLayer,
            'Light (grayscale)': this.lightLayer,
        };

        const overlayMaps = {
            'Cluster map': this.clusterLayer,
            'Heat map': this.heatLayer

        };

        this.map.removeControl(this.layControl);
        this.layControl = L.control.layers(baseMaps, overlayMaps);
        this.layControl.addTo(this.map);
    }
}
