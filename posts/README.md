# posts/

Each post is a single markdown file in this folder, named `YYYY-MM-DD-slug.md`.

## Adding a new post

1. Create `posts/2026-04-19-my-new-post.md` with frontmatter:

   ```markdown
   ---
   title: My new post
   date: 2026-04-19
   tags: [ml, note]
   summary: One-line description that shows up in the list.
   ---

   Your markdown content goes here. **Bold**, *italic*, `code`, lists,
   headings, links — all standard.
   ```

2. Add an entry to `posts/index.json` (newest first):

   ```json
   {
     "slug": "2026-04-19-my-new-post",
     "title": "My new post",
     "date": "2026-04-19",
     "tags": ["ml", "note"],
     "summary": "One-line description that shows up in the list."
   }
   ```

   (The manifest exists because GitHub Pages can't list directories. The
   frontmatter and manifest should agree — easiest is to copy/paste.)

3. Commit and push. The site will pick it up on next load.

## Why this structure

- **Plain markdown** — edit in any editor, preview on github.com directly.
- **`slug` in the filename AND in the url** — `post.html?slug=2026-04-19-my-new-post`.
- **No build step** — the site is fully static; the browser fetches `index.json` and the `.md` files on demand.
