# {{project_title}}

A modern Vue.js application built with Vue 3, TypeScript, Vite, Tailwind CSS, and Pinia.

## Features

- **Vue 3**: The progressive JavaScript framework for building user interfaces
- **TypeScript**: Adds static typing to JavaScript to improve developer experience
- **Vite**: Next generation frontend tooling for faster development
- **Tailwind CSS**: A utility-first CSS framework for rapid UI development
- **Pinia**: Intuitive, type safe and flexible Store for Vue
- **Vue Router**: The official router for Vue.js

## Project Setup

```sh
# Install dependencies
bun install

# Start development server
bun run dev

# Build for production
bun run build

# Preview production build
bun run preview

# Type-check
bun run type-check

# Lint
bun run lint
```

## Project Structure

```
src/
├── assets/         # Static assets like CSS, images, fonts
├── components/     # Reusable Vue components
├── router/         # Vue Router configuration
├── stores/         # Pinia stores for state management
├── views/          # Page components
├── App.vue         # Root component
└── main.ts         # Application entry point
```

## Components

The project includes several pre-built components:

- **Button**: A customizable button component with different variants
- **Card**: A card component for displaying content in a contained format
- **Navbar**: A responsive navigation bar

## Environment Variables

The following environment variables can be configured in `.env` files:

- `VITE_APP_TITLE`: The application title
- `VITE_API_URL`: The base URL for API requests

## Recommended IDE Setup

- [VS Code](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur)

## Type Support For `.vue` Imports in TS

TypeScript cannot handle type information for `.vue` imports by default, so the `tsc` CLI is replaced with `vue-tsc` for type checking. In editors, the [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) extension is needed.

## Customization

- Edit `tailwind.config.js` to customize the design system
- Add new components in the `src/components` directory
- Create new views in the `src/views` directory
- Add new stores in the `src/stores` directory
