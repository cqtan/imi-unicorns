// Angular Dependencies
import { Component, OnInit, Input } from "@angular/core";

// Application Services
import { ModalService } from "./services/modal.service";
import { ImageService } from "./services/image.service";

// Data Model Interfaces
import { Category } from "./models/category.model";
import { StabiCategory } from './models/stabi-category.model';
import { ColorCategory } from './models/color-category.model';
import { iImage } from "./models/image.model";

@Component({
    host: {
        '(document:keydown)': 'escPressed($event)'
    },
    selector: 'modal-component',
    styleUrls: ['stylesheets/css/main.css'],
    templateUrl: './templates/modal-menu.component.html'
})

export class ModalMenuComponent implements OnInit {
    imageWidth: number = 0;
    imageHeight: number = 200;

    @Input() categories: Category[];
    @Input() stabiCategories: StabiCategory[];
    @Input() colors: ColorCategory[];

    clustersBox: boolean;
    genresBox: boolean;
    colorsBox: boolean;

    constructor(private modalService: ModalService, private imageService: ImageService) { }

    ngOnInit() {
        this.categories.forEach(category => {
            this.imageService.getFirstImageForFeature(category.feature)
                .subscribe((response: iImage) => {
                    category.path = response.path;
                })
        })

        this.stabiCategories.forEach(stabiCategory=> {
            this.imageService.getFristImageForSubject(stabiCategory.name)
                .subscribe((image: iImage) => {
                    stabiCategory.path = image.path;
                })
        })

        this.clustersBox = true;
        this.genresBox = false;
        this.colorsBox = false;

        // set the initial checkbox states
        (<any>document.getElementById('clusters')).checked = true;
        (<any>document.getElementById('genres')).checked = false;
        (<any>document.getElementById('colors')).checked = false;
    }

    // handle checkbox states
    trackState(type: string) {
        if (type === 'genres') {
            (<any>document.getElementById('clusters')).checked = false;
            (<any>document.getElementById('genres')).checked = true;
            (<any>document.getElementById('colors')).checked = false;

            this.clustersBox = false;
            this.genresBox = true;
            this.colorsBox = false;
        }

        if (type === 'clusters') {
            (<any>document.getElementById('clusters')).checked = true;
            (<any>document.getElementById('genres')).checked = false;
            (<any>document.getElementById('colors')).checked = false;

            this.clustersBox = true;
            this.genresBox = false;
            this.colorsBox = false;
        }

        if (type === 'colors') {
            (<any>document.getElementById('clusters')).checked = false;
            (<any>document.getElementById('genres')).checked = false;
            (<any>document.getElementById('colors')).checked = true;

            this.clustersBox = false;
            this.genresBox = false;
            this.colorsBox = true;
        }
    }

    // set the category and send it back to the parent component
    setCategory(category) {
        this.modalService.eventEmitter.emit({ category: category, type: 'category' });
    }

    // set the stabi category and send it back to the parent component
    setGenre(genre) {
        this.modalService.eventEmitter.emit({ genre: genre, type: 'genre' })
    }

    // set the color category and send it back to the parent component
    setColor(color) {
        this.modalService.eventEmitter.emit({ color: color, type: 'color' });
    }

    calculateImageWidth(image: HTMLImageElement) {
        let height: number = image.height;
        let width: number = image.width;

        return width * (this.imageHeight / height);
    }

    // listen to a esc event and destroy the modal when done
    escPressed(event: KeyboardEvent) {
        if (event.key === 'Escape') {
            this.modalService.destroy();
        }
    }

    // helper method to convert the hex values from the database into color strings
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
                if(color.toLowerCase() == hexID) 
                    return colors[color];
            }
    }
}
