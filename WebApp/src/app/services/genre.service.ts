import { Injectable } from '@angular/core'
import { HttpClient, HttpHeaders } from '@angular/common/http'

@Injectable()
export class GenreService {

    constructor(private httpClient: HttpClient) {
    }

    getSubjects() {
        let headers: HttpHeaders = new HttpHeaders();
        headers.append('Content-Type', 'application/json');

        return this.httpClient.get('/api/get-subjects', { headers: headers });
    }
}