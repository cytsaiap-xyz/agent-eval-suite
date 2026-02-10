# Task: Build a Kanban Board Application

Create a fully functional Kanban board in a single HTML file with no external dependencies.

## Your Task

Create `kanban.html` - a complete Kanban board application that works offline.

## Requirements

### Core Features

1. **Three Columns**
   - Todo
   - In Progress
   - Done
   - Clear visual separation with headers

2. **Add Cards**
   - Input field in each column to add new cards
   - Cards display a title
   - Enter key should add the card

3. **Delete Cards**
   - Each card has a delete button
   - Clicking delete removes the card

4. **Drag and Drop**
   - Drag cards between columns
   - Visual feedback during drag (opacity change)
   - Drop zones highlight when dragging over
   - **Must use pure JavaScript - no libraries**

### Advanced Features

5. **Inline Editing**
   - Double-click a card to edit its title
   - Press Enter to save
   - Press Escape to cancel
   - Click outside to save

6. **Undo/Redo**
   - Ctrl+Z (or Cmd+Z on Mac) to undo
   - Ctrl+Y (or Ctrl+Shift+Z) to redo
   - Support at least 20 operations in history
   - Works for: add, delete, move, edit

7. **LocalStorage Persistence**
   - Save board state on every change
   - Restore state when page loads
   - Handle corrupted data gracefully

8. **Keyboard Navigation**
   - Tab through cards
   - Enter to edit focused card
   - Arrow keys to move focus

### Polish

9. **CSS Animations**
   - Smooth transitions when cards move
   - Fade in effect for new cards

10. **Responsive Design**
    - Works on different screen sizes
    - Columns stack on mobile (< 768px)

11. **Accessibility**
    - Proper ARIA labels
    - Visible focus indicators

## Constraints

- **Single HTML file** - all HTML, CSS, and JavaScript in one file
- **No external dependencies** - no CDN links, no libraries
- **No build step** - just open the HTML file in a browser
- **Works offline** - no network requests

## Testing

Open `kanban.html` directly in a browser and verify:
- [ ] Can add cards to each column
- [ ] Can drag cards between columns
- [ ] Can delete cards
- [ ] Double-click to edit works
- [ ] Ctrl+Z undoes last action
- [ ] Ctrl+Y redoes
- [ ] Refresh page - cards persist
- [ ] Works without internet
