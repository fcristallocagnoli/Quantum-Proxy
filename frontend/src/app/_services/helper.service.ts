import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '@environments/environment';


const baseUrl = `${environment.apiUrl}/helpers`;

@Injectable({ providedIn: 'root' })
export class HelperService {

    constructor(private http: HttpClient) { }

    getAggregattion(collection: string, pipeline: any[]) {
        return this.http.post<any>(`${baseUrl}/aggregate`, { 'collection': collection, 'pipeline': pipeline });
    }

    countDocuments(collection: string) {
        return this.http.get<any>(`${baseUrl}/count-documents/${collection}`);
    }
}
