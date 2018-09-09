import { Injectable } from "@angular/core";
import { HttpClient, HttpHeaders } from '@angular/common/http'

/*
 * Class which is responsible in retrieving all book related things through http rest calls
 */
@Injectable()
export class BookService {
    constructor(private httpClient: HttpClient) { }

    public getBooksInRangeOfCategory(category: string, fromDate: number, toDate: number) {
        let headers = new HttpHeaders();
        headers.append('Content-Type', 'application/json');

        return this.httpClient.get('/api/books/category/' + category + '/' + fromDate + '/' + toDate, {headers: headers});
    }

    public getDateRangeOfCategory(category: string) {
        let headers = new HttpHeaders();
        headers.append('Content-Type', 'application/json');

        return this.httpClient.get('/api/books/category/' + category + '/range', {headers: headers});
    }

    public getDateRangeOfGenre(category: string) {
        let headers = new HttpHeaders();
        headers.append('Content-Type', 'application/json');

        return this.httpClient.get('/api/books/genre/' + category + '/range', {headers: headers});
    }

    public getBooksInRangeOfGenre(genre: string, fromDate: number, toDate: number) {
        let headers = new HttpHeaders();
        headers.append('Content-Type', 'application/json');

        return this.httpClient.get('/api/books/genre/' + genre + '/' + fromDate + '/' + toDate, {headers: headers});
    }

    public getBooksInRangeOfColor(hexID: string, fromDate: number, toDate: number) {
        let headers = new HttpHeaders();
        headers.append('Content-Type', 'application/json');

        return this.httpClient.get(escape('/api/books/color/' + hexID + '/' + fromDate + '/' + toDate), {headers: headers});
    }

    public getDateRangeOfColor(hexID: string) {
        let headers = new HttpHeaders();
        headers.append('Content-Type', 'application/json');

        return this.httpClient.get(escape('/api/books/color/' + hexID + '/range'), {headers: headers});
    }

    public getBookInformationForImage(identifier: string) {
        let headers = new HttpHeaders();
        headers.append('Content-Type', 'application/json');
        
        return this.httpClient.get('/api/book/identifier/' + identifier + '/information');
    }

    public getBooksInformation() {
        return this.httpClient.get('/api/booksInformation')
    }

    public getMinMax(){
        return this.httpClient.get('/api/min-max')
    }

}
