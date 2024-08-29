import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { DatabaseComponent } from './database.component';
import { ProvidersAdminComponent } from './providers-admin.component';
import { AddEditProviderComponent } from './add-edit-provider.component';

const routes: Routes = [
    { path: '', component: DatabaseComponent },
    { path: 'providers', component: ProvidersAdminComponent },
    { path: 'providers/add', component: AddEditProviderComponent },
    { path: 'providers/edit/:pid', component: AddEditProviderComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class DatabaseRoutingModule { }