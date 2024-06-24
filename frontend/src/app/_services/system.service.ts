import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { System } from '@app/_models/system';
import { environment } from '@environments/environment';

const baseUrl = `${environment.apiUrl}/backends`;

@Injectable({ providedIn: 'root' })
export class SystemService {

  constructor(private http: HttpClient) { }

  getAll() {
    return this.http.get<System[]>(baseUrl);
  }

  getByBid(bid: string) {
    return this.http.get<System>(`${baseUrl}/${bid}`);
  }

  refreshData(filter: any) {
    return this.http.post(`${baseUrl}/refresh`, { filter });
  }
}
