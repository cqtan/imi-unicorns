// Angular Depenedencies
import { Component, EventEmitter, Input, OnInit, Output, AfterViewInit, OnChanges } from "@angular/core";

// Application Services
import { CategoryService } from './services/category.service';
import { ColorService } from './services/color.service';
import { BookService } from "./services/book.service";
import { GenreService } from "./services/genre.service";
import { ModalService } from "./services/modal.service";

// Application Components
import { ModalMenuComponent } from "./modal-menu.component";

// Data Model Interfaces
import { Category } from './models/category.model';
import { StabiCategory } from './models/stabi-category.model';
import { ColorCategory } from './models/color-category.model';

@Component({
    selector: 'cluster-row',
    styleUrls: ['stylesheets/css/main.css'],
    templateUrl: './templates/cluster-row.component.html'
})

/**
* Component to display a single category of a cluster on the view
*/
export class ClusterRowComponent implements OnInit, OnChanges {

    // references to handle the component
    _ref: any = this;
    elementNumber: number;

    // arrays containing the information
    activePPNs: any;
    features: Category[];
    subjects: StabiCategory[];
    colors: ColorCategory[];

    // selected refenrece
    chosenCategory: Category;
    chosenGenre: StabiCategory;
    chosenColor: ColorCategory;

    eventSubscription: EventEmitter<any>;

    @Input() zoomFactor: number;
    @Input() sliderRange: number[];
    @Output() deleted: EventEmitter<boolean> = new EventEmitter();
    @Output() minMaxRange: EventEmitter<Object> = new EventEmitter();

    set setSliderRange(value: number[]) {
        if (this.sliderRange === value) return;
        this.sliderRange = value;
        this.changes();
    }

    set zoomFactorSetter(value: number){
        this.zoomFactor = value;
    };

    get getTimeSlider() {
        return this.sliderRange;
    }

    // constructor which instantiats the classes and variables
    constructor(private categoryService: CategoryService, private modalService: ModalService,
        private bookService: BookService, private genreService: GenreService, private colorService: ColorService) {
    }

    // listens to the initiation event of a component
    ngOnInit() {
        this.categoryService.getFeatures().subscribe((data: any) => this.features = data);
        this.genreService.getSubjects().subscribe((data: any) => this.subjects = data);
        this.colorService.getColors().subscribe((data:any) => this.colors = data);
    }

    // function which will listen to angular based change events
    ngOnChanges() {
        if (this.chosenCategory && this.sliderRange.length) {
            this.getActivePPNsForCluster(this.chosenCategory, this.sliderRange);
        }
        if (this.chosenGenre && this.sliderRange.length) {
            this.getActivePPNsForGenre(this.chosenGenre, this.sliderRange);
        }

        if (this.chosenColor && this.sliderRange.length) {
            this.getActivePPNsForColor(this.chosenColor, this.sliderRange);
        }
    }

    // custom change event listener
    changes() {
        if (this.chosenCategory && this.sliderRange.length) {
            this.getActivePPNsForCluster(this.chosenCategory, this.sliderRange);
        }

        if (this.chosenGenre && this.sliderRange.length) {
            this.getActivePPNsForGenre(this.chosenGenre, this.sliderRange);
        }

        if (this.chosenColor && this.sliderRange.length) {
            this.getActivePPNsForColor(this.chosenColor, this.sliderRange);
        }
    }

    // destroy the modal created by this component when called 
    destroyModal() {
        this.eventSubscription.unsubscribe();
        this.modalService.destroy();
    }

    // delete the created row and fire a confirmation event
    removeClusterRow() {
        this.deleted.emit();
        this._ref.destroy();
    }

    // creates the ModalMenuComponent and passes in the features, subject and colors from this components as categories, stabiCategories and colors into the ModalMenuComponent
    createModal() {
        // create modal
        this.modalService.init(ModalMenuComponent, { categories: this.features, stabiCategories: this.subjects, colors: this.colors }, {});

        // subscribe to the EventEmitter from the ModalService here and create a reference in class
        this.eventSubscription = this.modalService.eventEmitter.subscribe((elem: any) => {
            // unsubscribe the reference in class to fix reference mirage
            if (elem.type === "category") {
                // set category
                this.chosenCategory = elem.category;
                this.chosenGenre = null;
                this.chosenColor = null;

                if (this.getTimeSlider) {
                    this.getActivePPNsForCluster(this.chosenCategory, this.getTimeSlider);
                }

                this.bookService.getDateRangeOfCategory(elem.category.feature)
                    .subscribe(
                        success => {
                            this.minMaxRange.emit(success);
                        });

                this.eventSubscription.unsubscribe();
            }

            if (elem.type === "genre") {
                this.chosenGenre = elem.genre;
                this.chosenCategory = null;
                this.chosenColor = null;

                if (this.getTimeSlider) {
                    this.getActivePPNsForGenre(this.chosenGenre, this.getTimeSlider);
                }

                this.bookService.getDateRangeOfGenre(elem.genre.name)
                    .subscribe(
                        success => {
                            this.minMaxRange.emit(success);
                        });

                this.eventSubscription.unsubscribe();
            }

            if (elem.type === "color") {
                this.chosenColor = elem.color;
                this.chosenCategory = null;
                this.chosenGenre = null;

                if (this.getTimeSlider) {
                    this.getActivePPNsForColor(this.chosenColor, this.getTimeSlider);
                }

                this.bookService.getDateRangeOfColor(elem.color.name)
                    .subscribe(
                        success => {
                            this.minMaxRange.emit(success);
                        });
                this.eventSubscription.unsubscribe();
            }

            // destroy the currently created modal
            this.modalService.destroy();
        });
    }

    // get the active ppns for the chosen category based on the given time space
    getActivePPNsForCluster(cluster: Category, timeSlider: number[]) {
        this.bookService.getBooksInRangeOfCategory(cluster.feature, timeSlider[0], timeSlider[1])
            .subscribe(data => {
                this.activePPNs = data;
            })
    }

    // get the active ppns for the chosen stabi category based on the given time space
    getActivePPNsForGenre(genre: any, timeSlider: number[]) {
        this.bookService.getBooksInRangeOfGenre(genre.name, timeSlider[0], timeSlider[1])
            .subscribe(data => {
                this.activePPNs = data;
            });
    }

    // get the active ppns for the chosen color category based on the given time space
    getActivePPNsForColor(color: any, timeSlider: number[]) {
        this.bookService.getBooksInRangeOfColor(color.name, timeSlider[0], timeSlider[1])
            .subscribe(data => {
                this.activePPNs = data;
            });
    }

    // helper function to convert the hexIDs of the colors into css names
    getNamesForColor(hexID: string) {
        let colors  = {
                "#800000": "Maroon",
                "#8B0000": "DarkRed",
                "#B22222": "FireBrick",
                "#FF0000": "Red",
                "#FA8072": "Salmon",
                "#FF6347": "Tomato",
                "#FF7F50": "Coral",
                "#FF4500": "OrangeRed",
                "#D2691E": "Chocolate",
                "#F4A460": "SandyBrown",
                "#FF8C00": "DarkOrange",
                "#FFA500": "Orange",
                "#B8860B": "DarkGoldenrod",
                "#DAA520": "Goldenrod",
                "#FFD700": "Gold",
                "#808000": "Olive",
                "#FFFF00": "Yellow",
                "#9ACD32": "YellowGreen",
                "#ADFF2F": "GreenYellow",
                "#7FFF00": "Chartreuse",
                "#7CFC00": "LawnGreen",
                "#008000": "Green",
                "#00FF00": "Lime",
                "#32CD32": "LimeGreen",
                "#00FF7F": "SpringGreen",
                "#00FA9A": "MediumSpringGreen",
                "#40E0D0": "Turquoise",
                "#20B2AA": "LightSeaGreen",
                "#48D1CC": "MediumTurquoise",
                "#008080": "Teal",
                "#008B8B": "DarkCyan",
                "#00FFFF": "Cyan",
                "#00CED1": "DarkTurquoise",
                "#00BFFF": "DeepSkyBlue",
                "#1E90FF": "DodgerBlue",
                "#4169E1": "RoyalBlue",
                "#000080": "Navy",
                "#00008B": "DarkBlue",
                "#0000CD": "MediumBlue",
                "#0000FF": "Blue",
                "#8A2BE2": "BlueViolet",
                "#9932CC": "DarkOrchid",
                "#9400D3": "DarkViolet",
                "#800080": "Purple",
                "#8B008B": "DarkMagenta",
                "#FF00FF": "Magenta",
                "#C71585": "MediumVioletRed",
                "#FF1493": "DeepPink",
                "#FF69B4": "HotPink",
                "#DC143C": "Crimson",
                "#A52A2A": "Brown",
                "#CD5C5C": "IndianRed",
                "#BC8F8F": "RosyBrown",
                "#F08080": "LightCoral",
                "#FFFAFA": "Snow",
                "#FFE4E1": "MistyRose",
                "#E9967A": "DarkSalmon",
                "#FFA07A": "LightSalmon",
                "#A0522D": "Sienna",
                "#FFF5EE": "SeaShell",
                "#8B4513": "SaddleBrown",
                "#FFDAB9": "Peachpuff",
                "#CD853F": "Peru",
                "#FAF0E6": "Linen",
                "#FFE4C4": "Bisque",
                "#DEB887": "Burlywood",
                "#D2B48C": "Tan",
                "#FAEBD7": "AntiqueWhite",
                "#FFDEAD": "NavajoWhite",
                "#FFEBCD": "BlanchedAlmond",
                "#FFEFD5": "PapayaWhip",
                "#FFE4B5": "Moccasin",
                "#F5DEB3": "Wheat",
                "#FDF5E6": "Oldlace",
                "#FFFAF0": "FloralWhite",
                "#FFF8DC": "Cornsilk",
                "#F0E68C": "Khaki",
                "#FFFACD": "LemonChiffon",
                "#EEE8AA": "PaleGoldenrod",
                "#BDB76B": "DarkKhaki",
                "#F5F5DC": "Beige",
                "#FAFAD2": "LightGoldenrodYellow",
                "#FFFFE0": "LightYellow",
                "#FFFFF0": "Ivory",
                "#6B8E23": "OliveDrab",
                "#556B2F": "DarkOliveGreen",
                "#8FBC8F": "DarkSeaGreen",
                "#006400": "DarkGreen",
                "#228B22": "ForestGreen",
                "#90EE90": "LightGreen",
                "#98FB98": "PaleGreen",
                "#F0FFF0": "Honeydew",
                "#2E8B57": "SeaGreen",
                "#3CB371": "MediumSeaGreen",
                "#F5FFFA": "Mintcream",
                "#66CDAA": "MediumAquamarine",
                "#7FFFD4": "Aquamarine",
                "#2F4F4F": "DarkSlateGray",
                "#AFEEEE": "PaleTurquoise",
                "#E0FFFF": "LightCyan",
                "#F0FFFF": "Azure",
                "#5F9EA0": "CadetBlue",
                "#B0E0E6": "PowderBlue",
                "#ADD8E6": "LightBlue",
                "#87CEEB": "SkyBlue",
                "#87CEFA": "LightskyBlue",
                "#4682B4": "SteelBlue",
                "#F0F8FF": "AliceBlue",
                "#708090": "SlateGray",
                "#778899": "LightSlateGray",
                "#B0C4DE": "LightsteelBlue",
                "#6495ED": "CornflowerBlue",
                "#E6E6FA": "Lavender",
                "#F8F8FF": "GhostWhite",
                "#191970": "MidnightBlue",
                "#6A5ACD": "SlateBlue",
                "#483D8B": "DarkSlateBlue",
                "#7B68EE": "MediumSlateBlue",
                "#9370DB": "MediumPurple",
                "#4B0082": "Indigo",
                "#BA55D3": "MediumOrchid",
                "#DDA0DD": "Plum",
                "#EE82EE": "Violet",
                "#D8BFD8": "Thistle",
                "#DA70D6": "Orchid",
                "#FFF0F5": "LavenderBlush",
                "#DB7093": "PaleVioletRed",
                "#FFC0CB": "Pink",
                "#FFB6C1": "LightPink",
                "#000000": "Black",
                "#696969": "DimGray",
                "#808080": "Gray",
                "#A9A9A9": "DarkGray",
                "#C0C0C0": "Silver",
                "#D3D3D3": "LightGrey",
                "#DCDCDC": "Gainsboro",
                "#F5F5F5": "WhiteSmoke",
                "#FFFFFF": "White"
            }

            for (let color in colors) {
                if(color.toLowerCase() == hexID) {
                        return colors[color];
                    }
            }
    }
}

