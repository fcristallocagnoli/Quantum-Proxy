import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ProvidersComponent } from './providers.component';
import { ViewProviderComponent } from './view-provider.component';


const routes: Routes = [
    { path: '', component: ProvidersComponent },
    { path: ':pid', component: ViewProviderComponent },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ProvidersRoutingModule { }