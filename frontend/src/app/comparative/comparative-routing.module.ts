import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { ComparativeComponent } from './comparative.component';
import { ViewComparativeComponent } from './view-comparative.component';


const routes: Routes = [
    { path: '', component: ComparativeComponent },
    { path: ':versus', component: ViewComparativeComponent },
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class ComparativeRoutingModule { }