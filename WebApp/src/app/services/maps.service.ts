import { Injectable } from "@angular/core";
import { Http, Headers } from "@angular/http"


@Injectable()
export class MapService {
    constructor(private http: Http) {

    }

    getlatLong() {
        return this.http.get('/api/maps-long-lat')
            .toPromise()
            .then(response => response.json())
            .catch((error) => console.log('error while getting map information: ', error));
    }
}
