import { Component, Input } from '@angular/core';

@Component({
    selector: 'theme',
    templateUrl: './theme.component.html',
})
export class ThemeComponent {
    @Input({ alias: 'theme' }) activeTheme: string;

    setStoredTheme(theme: string): void {
        localStorage.setItem('theme', theme);
    }

    setTheme(theme: string): void {
        if (theme === 'auto') {
            document.documentElement.setAttribute('data-bs-theme', window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
        } else {
            document.documentElement.setAttribute('data-bs-theme', theme);
        }
    }

    toggleTheme(theme: string): void {
        this.setStoredTheme(theme);
        this.setTheme(theme);
        this.activeTheme = theme;
    }
}
