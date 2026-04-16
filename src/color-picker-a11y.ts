/**
 * Accessibility improvements for the color picker.
 *
 * Split the single hue wheel into separate hue + saturation sliders
 * with a live preview swatch, so colorblind users can distinguish
 * their selection without relying on hue alone.
 */
export interface ColorPickerConfig {
  readonly hueLabel: string;
  readonly saturationLabel: string;
  readonly previewAriaLabel: string;
}

export const createAccessibleColorPicker = (
  container: HTMLElement,
  config: ColorPickerConfig = {
    hueLabel: 'Hue',
    saturationLabel: 'Saturation',
    previewAriaLabel: 'Selected color preview',
  },
): { destroy: () => void } => {
  const hueSlider = document.createElement('input');
  hueSlider.type = 'range';
  hueSlider.min = '0';
  hueSlider.max = '360';
  hueSlider.setAttribute('aria-label', config.hueLabel);

  const satSlider = document.createElement('input');
  satSlider.type = 'range';
  satSlider.min = '0';
  satSlider.max = '100';
  satSlider.setAttribute('aria-label', config.saturationLabel);

  const preview = document.createElement('div');
  preview.setAttribute('role', 'status');
  preview.setAttribute('aria-label', config.previewAriaLabel);
  preview.style.width = '48px';
  preview.style.height = '48px';
  preview.style.borderRadius = '8px';

  const update = () => {
    const hue = Number(hueSlider.value);
    const sat = Number(satSlider.value);
    preview.style.backgroundColor = `hsl(${hue}, ${sat}%, 50%)`;
  };

  hueSlider.addEventListener('input', update);
  satSlider.addEventListener('input', update);

  container.append(hueSlider, satSlider, preview);
  update();

  return {
    destroy: () => {
      hueSlider.remove();
      satSlider.remove();
      preview.remove();
    },
  };
};
