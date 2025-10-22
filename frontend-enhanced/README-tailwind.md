Quick fixes for Tailwind setup

Problem:

- `npx tailwindcss init -p` failed due to an engine mismatch on this machine (Node v18 vs packages requiring Node >=20).

What I added:

- `tailwind.config.cjs` - content paths and minimal config
- `postcss.config.cjs` - loads tailwindcss and autoprefixer
- `src/index.css` - prepended Tailwind directives to the existing CSS

Options to proceed:

1. Upgrade Node to >= 20 (recommended)
   - Install Node 20 via nvm-windows or Node installer and re-run:

```powershell
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
npm run dev
```

2. Use Tailwind CLI from node_modules without npx (works without global npx invocation):
   - Run the Tailwind CLI directly via the installed package binary (Windows PowerShell):

```powershell
.
# From project root
node_modules\.bin\tailwindcss -i ./src/index.css -o ./dist/output.css --watch
```

3. Continue development without full init: the `tailwind.config.cjs` and `postcss.config.cjs` files are present so most build tools (Vite) will pick them up. If you see CSS not applying, run the CLI command above or upgrade Node.

If you'd like, I can:

- Upgrade the project's `engines` field or add an `.nvmrc` with recommended Node version.
- Add an npm script to run the tailwind CLI to avoid typing the long command.
