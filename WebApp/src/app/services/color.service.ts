import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http'

@Injectable()
export class ColorService {
    constructor(private httpClient: HttpClient) {
    }

    getColors() {
        return this.httpClient.get('/api/get-colors', {});
    }
}
