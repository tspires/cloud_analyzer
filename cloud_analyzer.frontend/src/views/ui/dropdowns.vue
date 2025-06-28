<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard title="Single Button Dropdowns" id="single-button">
            <div class="d-flex flex-wrap gap-3 mt-3">
              <b-dropdown text="Dropdown button">
                <b-dropdown-item>Action</b-dropdown-item>
                <b-dropdown-item>Another action</b-dropdown-item>
                <b-dropdown-item>Something else here</b-dropdown-item>
              </b-dropdown>

              <b-dropdown toggle-class="btn-secondary p-0 m-0" no-caret>
                <template #button-content>
                  <a href="#" class="btn btn-secondary dropdown-toggle"> Dropdown link </a>
                </template>
                <b-dropdown-item>Action</b-dropdown-item>
                <b-dropdown-item>Another action</b-dropdown-item>
                <b-dropdown-item>Something else here</b-dropdown-item>
              </b-dropdown>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Single Button Variant Dropdowns" id="single-button-variant">
            <div class="d-flex flex-wrap gap-2 mt-3">
              <b-dropdown variant="primary" text="Primary">
                <b-dropdown-item>Action</b-dropdown-item>
                <b-dropdown-item>Another action</b-dropdown-item>
                <b-dropdown-item>Something else here</b-dropdown-item>
                <b-dropdown-divider/>
                <b-dropdown-item>Separated link</b-dropdown-item>
              </b-dropdown>

              <b-dropdown variant="secondary" text="Secondary">
                <b-dropdown-item>Action</b-dropdown-item>
                <b-dropdown-item>Another action</b-dropdown-item>
                <b-dropdown-item>Something else here</b-dropdown-item>
                <b-dropdown-divider/>
                <b-dropdown-item>Separated link</b-dropdown-item>
              </b-dropdown>

              <b-dropdown variant="success" text="Success">
                <b-dropdown-item>Action</b-dropdown-item>
                <b-dropdown-item>Another action</b-dropdown-item>
                <b-dropdown-item>Something else here</b-dropdown-item>
                <b-dropdown-divider/>
                <b-dropdown-item>Separated link</b-dropdown-item>
              </b-dropdown>

              <b-dropdown variant="info" text="Info">
                <b-dropdown-item>Action</b-dropdown-item>
                <b-dropdown-item>Another action</b-dropdown-item>
                <b-dropdown-item>Something else here</b-dropdown-item>
                <b-dropdown-divider/>
                <b-dropdown-item>Separated link</b-dropdown-item>
              </b-dropdown>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Split Button Dropdowns" id="split-button">
            <div class="d-flex flex-wrap gap-2 mt-3">
              <b-dropdown split variant="primary" text="Primary" class="me-2">
                <b-dropdown-item href="#">Action</b-dropdown-item>
                <b-dropdown-item href="#">Another action</b-dropdown-item>
                <b-dropdown-item href="#">Something else here</b-dropdown-item>
                <b-dropdown-divider/>
                <b-dropdown-item href="#">Separated link</b-dropdown-item>
              </b-dropdown>

              <b-dropdown split variant="secondary" text="Secondary" class="me-2">
                <b-dropdown-item href="#">Action</b-dropdown-item>
                <b-dropdown-item href="#">Another action</b-dropdown-item>
                <b-dropdown-item href="#">Something else here</b-dropdown-item>
                <b-dropdown-divider/>
                <b-dropdown-item href="#">Separated link</b-dropdown-item>
              </b-dropdown>

              <b-dropdown split variant="success" text="Success" class="me-2">
                <b-dropdown-item href="#">Action</b-dropdown-item>
                <b-dropdown-item href="#">Another action</b-dropdown-item>
                <b-dropdown-item href="#">Something else here</b-dropdown-item>
                <b-dropdown-divider/>
                <b-dropdown-item href="#">Separated link</b-dropdown-item>
              </b-dropdown>

              <b-dropdown split variant="info" text="Info" class="me-2">
                <b-dropdown-item href="#">Action</b-dropdown-item>
                <b-dropdown-item href="#">Another action</b-dropdown-item>
                <b-dropdown-item href="#">Something else here</b-dropdown-item>
                <b-dropdown-divider/>
                <b-dropdown-item href="#">Separated link</b-dropdown-item>
              </b-dropdown>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Dark Dropdowns" id="dark-dropdown">
            <b-dropdown variant="primary" text="Dark Dropdown" menu-class="dropdown-menu-dark" class="mt-3">
              <b-dropdown-item>Action</b-dropdown-item>
              <b-dropdown-item>Another action</b-dropdown-item>
              <b-dropdown-item>Something else here</b-dropdown-item>
              <b-dropdown-divider/>
              <b-dropdown-item>Separated link</b-dropdown-item>
            </b-dropdown>
          </UIComponentCard>

          <UIComponentCard title="Dropdown Direction" id="direction">
            <div class="d-flex flex-wrap gap-2 mt-3">
              <b-dropdown variant="primary" text="Drop Down">
                <b-dropdown-item>Action</b-dropdown-item>
                <b-dropdown-item>Another action</b-dropdown-item>
                <b-dropdown-item>Something else here</b-dropdown-item>
                <b-dropdown-divider/>
                <b-dropdown-item>Separated link</b-dropdown-item>
              </b-dropdown>

              <DropDown custom-class="btn-group dropup">
                <button type="button" class="btn btn-secondary dropdown-toggle" data-bs-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">Drop Up
                </button>
                <ul class="dropdown-menu">
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Another action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Something else here</a>
                  </li>
                  <li>
                    <hr class="dropdown-divider"/>
                  </li>
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Separated link</a>
                  </li>
                </ul>
              </DropDown>

              <DropDown custom-class="btn-group dropstart">
                <button type="button" class="btn btn-info dropdown-toggle" data-bs-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">Drop Left
                </button>
                <ul class="dropdown-menu">
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Another action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Something else here</a>
                  </li>
                  <li>
                    <hr class="dropdown-divider"/>
                  </li>
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Separated link</a>
                  </li>
                </ul>
              </DropDown>

              <DropDown custom-class="btn-group dropend">
                <button type="button" class="btn btn-success dropdown-toggle" data-bs-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">Drop Right
                </button>
                <ul class="dropdown-menu">
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Another action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Something else here</a>
                  </li>
                  <li>
                    <hr class="dropdown-divider"/>
                  </li>
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Separated link</a>
                  </li>
                </ul>
              </DropDown>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Dropdown Menu Items" id="menu-items">
            <div class="d-flex flex-wrap gap-2 mt-3">
              <ul class="dropdown-menu show block position-static">
                <li>
                  <a class="dropdown-item" href="#">Regular link</a>
                </li>
                <li>
                  <a class="dropdown-item active" href="#" aria-current="true">Active link</a>
                </li>
                <li>
                  <a class="dropdown-item" href="#">Another link</a>
                </li>
              </ul>

              <ul class="dropdown-menu show block position-static">
                <li>
                  <a class="dropdown-item" href="#">Regular link</a>
                </li>
                <li>
                  <a class="dropdown-item disabled" href="#" aria-current="true">Active link</a>
                </li>
                <li>
                  <a class="dropdown-item" href="#">Another link</a>
                </li>
              </ul>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Dropdown options" id="dropdown-options">
            <div class="d-flex flex-wrap gap-2 mt-3">
              <div class="dropdown">
                <button type="button" class="btn btn-secondary dropdown-toggle" data-bs-toggle="dropdown"
                        aria-expanded="false" data-bs-offset="10,20">Offset
                </button>
                <ul class="dropdown-menu">
                  <li>
                    <a class="dropdown-item" href="#">Action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#">Another action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#">Something else here</a>
                  </li>
                </ul>
              </div>

              <div class="btn-group">
                <button type="button" class="btn btn-secondary">Reference</button>
                <button type="button" class="btn btn-secondary dropdown-toggle dropdown-toggle-split"
                        data-bs-toggle="dropdown" aria-expanded="false" data-bs-reference="parent">
                  <span class="visually-hidden">Toggle Dropdown</span>
                </button>
                <ul class="dropdown-menu">
                  <li>
                    <a class="dropdown-item" href="#">Action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#">Another action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#">Something else here</a>
                  </li>
                  <li>
                    <hr class="dropdown-divider"/>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#">Separated link</a>
                  </li>
                </ul>
              </div>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Auto close behavior" id="auto-close-behavior"
                           caption="By default, the dropdown menu is closed when clicking inside or outside the dropdown menu. You can use the <code>autoClose</code> option to change this behavior of the dropdown.">
            <div class="d-flex flex-wrap gap-2">
              <b-dropdown text="Default dropdown">
                <b-dropdown-item>Menu item</b-dropdown-item>
                <b-dropdown-item>Menu item</b-dropdown-item>
                <b-dropdown-item>Menu item</b-dropdown-item>
              </b-dropdown>

              <b-dropdown text="Clickable inside" auto-close="inside">
                <b-dropdown-item>Menu item</b-dropdown-item>
                <b-dropdown-item>Menu item</b-dropdown-item>
                <b-dropdown-item>Menu item</b-dropdown-item>
              </b-dropdown>

              <b-dropdown text="Clickable outside" auto-close="outside">
                <b-dropdown-item>Menu item</b-dropdown-item>
                <b-dropdown-item>Menu item</b-dropdown-item>
                <b-dropdown-item>Menu item</b-dropdown-item>
              </b-dropdown>

              <b-dropdown text="Manual close" :auto-close="false">
                <b-dropdown-item>Menu item</b-dropdown-item>
                <b-dropdown-item>Menu item</b-dropdown-item>
                <b-dropdown-item>Menu item</b-dropdown-item>
              </b-dropdown>
            </div>
          </UIComponentCard>

          <UIComponentCard title="Menu Content" id="menu-content">
            <p>Add a header to label sections of actions in any dropdown menu.</p>
            <p>Separate groups of related menu items with a divider.</p>
            <p>Place any freeform text within a dropdown menu with text and use spacing utilities. Note that you’ll
              likely need additional sizing styles to constrain the menu width.</p>
            <p>Put a form within a dropdown menu, or make it into a dropdown menu, and use margin or padding utilities
              to give it the negative space you require.</p>

            <div class="d-flex flex-wrap gap-2">
              <DropDown class="dropdown">
                <button class="btn btn-primary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">Dropdown Header
                </button>
                <ul class="dropdown-menu">
                  <li>
                    <a class="dropdown-header">Dropdown header</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="javascript:void(0);">Another action</a>
                  </li>
                </ul>
              </DropDown>

              <DropDown custom-class="dropdown">
                <button class="btn btn-info dropdown-toggle" type="button" data-bs-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">Dropdown Divider
                </button>
                <ul class="dropdown-menu">
                  <li>
                    <a class="dropdown-item" href="#">Action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#">Another action</a>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#">Something else here</a>
                  </li>
                  <li>
                    <hr class="dropdown-divider"/>
                  </li>
                  <li>
                    <a class="dropdown-item" href="#">Separated link</a>
                  </li>
                </ul>
              </DropDown>

              <DropDown custom-class="dropdown">
                <button class="btn btn-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">Dropdown Text
                </button>
                <div class="dropdown-menu dropdown-lg p-3">
                  <p>Some example text that's free-flowing within the dropdown menu.</p>
                  <p class="mb-0">And this is more example text.</p>
                </div>
              </DropDown>

              <DropDown custom-class="dropdown">
                <button class="btn btn-success dropdown-toggle" type="button" data-bs-toggle="dropdown"
                        aria-haspopup="true" aria-expanded="false">Dropdown Menu Forms
                </button>
                <b-form class="dropdown-menu dropdown-lg p-3">
                  <div class="mb-3">
                    <b-form-group label="Email address">
                      <b-form-input id="exampleDropdownFormEmail" placeholder="email@example.com"/>
                    </b-form-group>
                  </div>
                  <div class="mb-3">
                    <b-form-group label="Password">
                      <b-form-input id="exampleDropdownFormPassword" placeholder="Password"/>
                    </b-form-group>
                  </div>
                  <div class="mb-3">
                    <b-form-checkbox id="dropdownCheck" name="dropdownCheck"> Remember me</b-form-checkbox>
                  </div>
                  <b-button type="submit" variant="primary"> Sign in</b-button>
                </b-form>
              </DropDown>
            </div>
          </UIComponentCard>
        </b-col>

        <b-col xl="3">
          <AnchorNavigation :elements="anchorNavigation"/>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script lang="ts" setup>
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import AnchorNavigation from '@/components/AnchorNavigation.vue'
import UIComponentCard from '@/components/UIComponentCard.vue'
import DropDown from '@/components/DropDown.vue'

const anchorNavigation = [
  {
    id: 'single-button',
    title: 'Single Button Dropdowns'
  },
  {
    id: 'single-button-variant',
    title: 'Single Button Variant Dropdowns'
  },
  {
    id: 'split-button',
    title: 'Split Button Dropdowns'
  },
  {
    id: 'dark-dropdown',
    title: 'Dark Dropdown'
  },
  {
    id: 'direction',
    title: 'Dropdown Direction'
  },
  {
    id: 'menu-items',
    title: 'Dropdown Menu Items'
  },
  {
    id: 'dropdown-options',
    title: 'Dropdown Options'
  },
  {
    id: 'auto-close-behavior',
    title: 'Auto Close Behavior'
  },
  {
    id: 'menu-content',
    title: 'Menu content'
  }
]
</script>
