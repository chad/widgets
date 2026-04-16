/**
 * Fix drop-target flicker on slow machines.
 *
 * The requestAnimationFrame debounce prevents the drop zone from
 * toggling visibility faster than the compositor can paint, which
 * was the root cause of the flicker reported in sprint planning.
 */
export const stabilizeDropTarget = (element: HTMLElement): (() => void) => {
  let frameId: number | null = null;
  const onDragOver = (event: DragEvent) => {
    event.preventDefault();
    if (frameId !== null) {
      cancelAnimationFrame(frameId);
    }
    element.classList.add('drop-active');
    frameId = requestAnimationFrame(() => {
      frameId = null;
    });
  };
  const onDragLeave = () => {
    if (frameId !== null) {
      cancelAnimationFrame(frameId);
      frameId = null;
    }
    element.classList.remove('drop-active');
  };
  element.addEventListener('dragover', onDragOver);
  element.addEventListener('dragleave', onDragLeave);
  return () => {
    element.removeEventListener('dragover', onDragOver);
    element.removeEventListener('dragleave', onDragLeave);
    if (frameId !== null) {
      cancelAnimationFrame(frameId);
    }
  };
};
