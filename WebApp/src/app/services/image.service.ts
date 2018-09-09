import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from "@angular/common/http"

@Injectable()
export class ImageService {
    constructor(private httpClient: HttpClient) {

    }

    getImageForObjectID(objectID: string) {
        return this.httpClient.get('api/image/' + objectID);
    }

    getImageForFeature(feature: string) {
        let headers: HttpHeaders = new HttpHeaders()

        return this.httpClient.get('/api/category/' + feature + '/images')
    }

    getFirstImageForFeature(feature: string) {
        let headers: HttpHeaders = new HttpHeaders();

        return this.httpClient.get('/api/category/' + feature + '/first-image')
    }

    getImageForSubject(subject: string) {
        let headers: HttpHeaders = new HttpHeaders()
        headers.append('Content-Type', 'application/json');

        return this.httpClient.get('/api/genre/' + subject + '/images')
    }

    getFristImageForSubject(subject: string) {
        let headers: HttpHeaders = new HttpHeaders();
        headers.append('Content-Type', 'application/json');

        return this.httpClient.get('/api/genre/' + subject + '/first-image')
    }

    getImageForColor(color: string) {
        let headers: HttpHeaders = new HttpHeaders()

        return this.httpClient.get(escape('/api/color/' + color + '/images'))
    }
}
