import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';

import { Provider } from '@app/_models';
import { environment } from '@environments/environment';

const baseUrl = `${environment.apiUrl}/providers`;


@Injectable({ providedIn: 'root' })
export class ProviderService {

  constructor(private http: HttpClient) { }

  getAll(projection: any = null) {
    return this.http.post<Provider[]>(`${baseUrl}/custom-query`, { ...projection });
  }

  getByPid(pid: string) {
    return this.http.get<Provider>(`${baseUrl}/${pid}`);
  }

  create(params: any) {
    return this.http.post(baseUrl, params);
  }

  update(pid: string, params: any) {
    return this.http.put(`${baseUrl}/${pid}`, params);
  }

  deleteByPid(pid: string) {
    return this.http.delete(`${baseUrl}/${pid}`);
  }
}
