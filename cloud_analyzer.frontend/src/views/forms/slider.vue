<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard id="basic-range" title="Basic Range Slider">
            <div class="mt-3">
              <div id="rangeslider_basic"></div>
            </div>
          </UIComponentCard>

          <UIComponentCard id="vertical-range" title="Vertical Range Slider">
            <div class="mt-3">
              <div id="rangeslider_vertical" style="height: 150px"></div>
            </div>
          </UIComponentCard>

          <UIComponentCard id="multi-range" title="Multi Elements Range">
            <div class="mt-3">
              <div id="rangeslider_multielement"></div>
            </div>
          </UIComponentCard>

          <UIComponentCard id="colorpicker-range" title="Colorpicker">
            <div class="mt-3">
              <div class="sliders" id="red"></div>
              <div class="sliders" id="green"></div>
              <div class="sliders" id="blue"></div>

              <div id="result"></div>
            </div>
          </UIComponentCard>

          <UIComponentCard id="value-range" title="Value Range Slider">
            <div class="mt-3">
              <div id="nonlinear"></div>
              <div class="d-flex justify-content-between">
                <div class="example-val" id="lower-value"></div>
                <div class="example-val" id="upper-value"></div>
              </div>
            </div>
          </UIComponentCard>

          <UIComponentCard id="locking-together" title="Locking Sliders Together">
            <div class="mt-3">
              <div class="slider" id="slider1"></div>
              <span class="example-val mt-2" id="slider1-span"></span>

              <div class="slider" id="slider2"></div>
              <span class="example-val mt-2" id="slider2-span"></span>

              <b-button id="lockbutton" variant="primary"> Lock</b-button>
            </div>
          </UIComponentCard>

          <UIComponentCard id="tooltip" title="Tooltip">
            <div class="p-3">
              <div class="slider" id="slider-merging-tooltips"></div>
            </div>
          </UIComponentCard>

          <UIComponentCard id="soft-limits" title="Soft Limits">
            <div class="mb-3 pb-3">
              <div class="slider" id="soft"></div>
            </div>
          </UIComponentCard>

        </b-col>

        <b-col xl="3">
          <AnchorNavigation :elements="anchorNavigation" />
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import noUiSlider from 'nouislider';
import type { Options } from 'nouislider';
import wNumb from 'wnumb';
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import AnchorNavigation from '@/components/AnchorNavigation.vue';
import UIComponentCard from "@/components/UIComponentCard.vue";

onMounted(() => {
  // Basic
  const basicSlider = document.getElementById('rangeslider_basic');
  if (basicSlider) {
    noUiSlider.create(basicSlider, {
      start: 127,
      connect: 'lower',
      range: {
        min: 0,
        max: 255
      }
    } as Options);
  }

  // vertical
  const verticalRangeSlider = document.getElementById('rangeslider_vertical');
  if (verticalRangeSlider)
    noUiSlider.create(verticalRangeSlider, {
      start: [60, 160],
      connect: true,
      orientation: 'vertical',
      range: {
        min: 0,
        max: 200
      }
    });

  // multi range handle
  const multiElementSlider = document.getElementById('rangeslider_multielement');
  if (multiElementSlider)
    noUiSlider.create(multiElementSlider, {
      start: [20, 80],
      connect: true,
      range: {
        min: 0,
        max: 100
      }
    });

  // Colorpicker
  const resultElement = document.getElementById('result');
  const sliders = document.getElementsByClassName('sliders');
  const colors = [0, 0, 0];
  if (sliders && resultElement)
    [].slice.call(sliders).forEach(function (slider: any, index) {
      noUiSlider.create(slider, {
        start: 127,
        connect: [true, false],
        orientation: 'vertical',
        range: {
          min: 0,
          max: 255
        },
        format: wNumb({
          decimals: 0
        })
      } as Options);

      // Bind the color changing function to the update event.
      slider.noUiSlider.on('update', function () {
        colors[index] = slider.noUiSlider.get();

        let color = 'rgb(' + colors.join(',') + ')';

        resultElement.style.background = color;
        resultElement.style.color = color;
      });
    });

  // Non linear slider
  const nonLinearSlider = document.getElementById('nonlinear') as any;
  if (nonLinearSlider) {
    noUiSlider.create(nonLinearSlider, {
      connect: true,
      behaviour: 'tap',
      start: [500, 4000],
      range: {
        // Starting at 500, step the value by 500,
        // until 4000 is reached. From there, step by 1000.
        min: [0],
        '10%': [500, 500],
        '50%': [4000, 1000],
        max: [10000]
      }
    } as Options);

    const nodes = [
      document.getElementById('lower-value'), // 0
      document.getElementById('upper-value') // 1
    ] as HTMLElement[];

    // Display the slider value and how far the handle moved
    // from the left edge of the slider.
    nonLinearSlider.noUiSlider.on('update', function (values: string, handle: number, positions: number[]) {
      nodes[handle].innerHTML = values[handle] + ', ' + positions[handle].toFixed(2) + '%';
    });
  }

  // Locking sliders together
  let lockedState = false;
  let lockedSlider = false;
  let lockedValues = [60, 80];

  const slider1 = document.getElementById('slider1') as any;
  const slider2 = document.getElementById('slider2') as any;

  const lockButton = document.getElementById('lockbutton') as any;
  const slider1Value = document.getElementById('slider1-span') as any;
  const slider2Value = document.getElementById('slider2-span') as any;

  // When the button is clicked, the locked state is inverted.
  if (lockButton)
    lockButton.addEventListener('click', function () {
      lockedState = !lockedState;
      // this.textContent = lockedState ? 'unlock' : 'lock';
    });

  function crossUpdate(value: number, slider: any) {
    // If the sliders aren't interlocked, don't
    // cross-update.
    if (!lockedState) return;

    // Select whether to increase or decrease
    // the other slider value.
    let a = slider1 === slider ? 0 : 1;

    // Invert a
    let b = a ? 0 : 1;

    // Offset the slider value.
    value -= lockedValues[b] - lockedValues[a];

    // Set the value
    slider.noUiSlider.set(value);
  }

  noUiSlider.create(slider1, {
    start: 60,

    // Disable animation on value-setting,
    // so the sliders respond immediately.
    animate: false,
    range: {
      min: 50,
      max: 100
    }
  } as Options);

  noUiSlider.create(slider2, {
    start: 80,
    animate: false,
    range: {
      min: 50,
      max: 100
    }
  } as Options);

  if (slider1 && slider2) {
    slider1.noUiSlider.on('update', function (values: string, handle: number) {
      slider1Value.innerHTML = values[handle];
    });
    slider2.noUiSlider.on('update', function (values: string, handle: number) {
      slider2Value.innerHTML = values[handle];
    });

    function setLockedValues() {
      lockedValues = [Number(slider1?.noUiSlider.get()), Number(slider2?.noUiSlider.get())];
    }

    slider1.noUiSlider.on('change', setLockedValues);
    slider2.noUiSlider.on('change', setLockedValues);

    slider1.noUiSlider.on('slide', function (values: number[], handle: number) {
      crossUpdate(values[handle], slider2);
    });

    slider2.noUiSlider.on('slide', function (values: number[], handle: number) {
      crossUpdate(values[handle], slider1);
    });
  }

  // tooltip
  const mergingTooltipSlider = document.getElementById('slider-merging-tooltips');
  if (mergingTooltipSlider) {
    noUiSlider.create(mergingTooltipSlider, {
      start: [20, 75],
      connect: true,
      tooltips: [true, true],
      range: {
        min: 0,
        max: 100
      }
    });

    mergeTooltips(mergingTooltipSlider, 5, ' - ');
  }

  /**
   * @param slider HtmlElement with an initialized slider
   * @param threshold Minimum proximity (in percentages) to merge tooltips
   * @param separator String joining tooltips
   */
  function mergeTooltips(slider: any, threshold: number, separator: string) {
    let textIsRtl = getComputedStyle(slider).direction === 'rtl';
    let isRtl = slider.noUiSlider.options.direction === 'rtl';
    let isVertical = slider.noUiSlider.options.orientation === 'vertical';
    let tooltips = slider.noUiSlider.getTooltips();
    let origins = slider.noUiSlider.getOrigins();

    // Move tooltips into the origin element. The default stylesheet handles this.
    tooltips.forEach(function (tooltip: string, index: string) {
      if (tooltip) {
        origins[index].appendChild(tooltip);
      }
    });
    if (slider)
      slider.noUiSlider.on('update', function (values: string[], positions: any) {
        let pools: any = [[]];
        let poolPositions: any = [[]];
        let poolValues: any = [[]];
        let atPool = 0;

        // Assign the first tooltip to the first pool, if the tooltip is configured
        if (tooltips[0]) {
          pools[0][0] = 0;
          poolPositions[0][0] = positions[0];
          poolValues[0][0] = values[0];
        }

        for (let i = 1; i < positions.length; i++) {
          if (!tooltips[i] || positions[i] - positions[i - 1] > threshold) {
            atPool++;
            pools[atPool] = [];
            poolValues[atPool] = [];
            poolPositions[atPool] = [];
          }

          if (tooltips[i]) {
            pools[atPool].push(i);
            poolValues[atPool].push(values[i]);
            poolPositions[atPool].push(positions[i]);
          }
        }

        pools.forEach(function (pool: string, poolIndex: number) {
          let handlesInPool = pool.length;

          for (let j = 0; j < handlesInPool; j++) {
            let handleNumber = pool[j];

            if (j === handlesInPool - 1) {
              let offset = 0;

              poolPositions[poolIndex].forEach(function (value: number) {
                offset += 1000 - value;
              });

              let direction = isVertical ? 'bottom' : 'right';
              let last = isRtl ? 0 : handlesInPool - 1;
              let lastOffset = 1000 - poolPositions[poolIndex][last];
              offset = (textIsRtl && !isVertical ? 100 : 0) + offset / handlesInPool - lastOffset;

              // Center this tooltip over the affected handles
              tooltips[handleNumber].innerHTML = poolValues[poolIndex].join(separator);
              tooltips[handleNumber].style.display = 'block';
              tooltips[handleNumber].style[direction] = offset + '%';
            } else {
              // Hide this tooltip
              tooltips[handleNumber].style.display = 'none';
            }
          }
        });
      });
  }

  // Soft limits
  const softSlider = document.getElementById('soft') as any;
  if (softSlider) {
    noUiSlider.create(softSlider, {
      start: 50,
      range: {
        min: 0,
        max: 100
      },
      pips: {
        mode: 'values',
        values: [20, 80],
        density: 4
      }
    } as Options);

    softSlider.noUiSlider.on('change', function (values: number[], handle: number) {
      if (values[handle] < 20) {
        softSlider.noUiSlider.set(20);
      } else if (values[handle] > 80) {
        softSlider.noUiSlider.set(80);
      }
    });
  }
});

const anchorNavigation = [
  {
    id: 'basic-range',
    title: 'Basic Range Slider'
  },
  {
    id: 'vertical-range',
    title: 'Vertical Range Slider'
  },
  {
    id: 'multi-range',
    title: 'Multi Elements Range'
  },
  {
    id: 'colorpicker-range',
    title: 'Colorpicker'
  },
  {
    id: 'value-range',
    title: 'Value Range Slider'
  },
  {
    id: 'locking-together',
    title: 'Locking Sliders Together'
  },
  {
    id: 'tooltip',
    title: 'Tooltip'
  },
  {
    id: 'soft-limits',
    title: 'Soft Limits'
  }
];
</script>
