import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ProvidersComponent } from './providers.component';
import { ViewProviderComponent } from './view-provider.component';
import { SystemsComponent } from '@app/systems/systems.component';


const routes: Routes = [
    { path: '', component: ProvidersComponent },
    { path: ':pid', component: ViewProviderComponent },
    { path: ':pid/systems', component: SystemsComponent }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ProvidersRoutingModule { }