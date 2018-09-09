// Angular Dependencies
import { Component, EventEmitter, Input, OnChanges, OnInit, Output } from "@angular/core";

@Component({
    selector: 'time-slider',
    styleUrls: ['stylesheets/css/main.css'],
    templateUrl: './templates/time-slider.component.html'
})

/**
 * Component which will display our time line at the bottom of the image-view
 */
export class TimeSliderComponent implements OnInit, OnChanges {
    @Input('currentMinMax') currentMinMax: number[];
    @Output('range') rangeChanged = new EventEmitter<number[]>();

    // empty config object to fill it with new data when required
    config: any = { }

    constructor() { }

    ngOnInit() {
        this.config = {
            behaviour: 'drag',
            connect: true,
            step: 1,
            range: {
                min: this.currentMinMax[0],
                max: this.currentMinMax[1]
            },
            pips: {
                mode: 'count',
                density: 10,
                values: 3,
                stepped: true
            }
        }
    }

    ngOnChanges() {
        this.config.range.min = this.currentMinMax[0];
        this.config.range.max = this.currentMinMax[1];
    }

    debouncedChangeEvent = this.debounce(event => {
        this.rangeChanged.emit(event);
    }, 250, false)

    debounce(func, wait, immediate) {
        var timeout;
        return function () {
            let context = this, args = arguments;
            let later = function () {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            let callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    };
}
