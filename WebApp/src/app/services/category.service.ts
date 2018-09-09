import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from '@angular/common/http'

@Injectable()
export class CategoryService {
    constructor(private httpClient: HttpClient) {

    }

    // gets the categories from the mongo db
    getFeatures() {
        return this.httpClient.get('/api/get-features')
    }
}