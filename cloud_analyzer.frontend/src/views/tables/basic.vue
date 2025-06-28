<template>
  <VerticalLayout>
      <b-row>
        <b-col xl="9">
          <UIComponentCard id="basic" title="Basic Example">
            <b-table-simple responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="inverse" title="Variants">
            <b-table-simple responsive class="mb-0">
              <b-thead>
                <b-tr>
                  <b-th scope="col">Class</b-th>
                  <b-th scope="col">Heading</b-th>
                  <b-th scope="col">Heading</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr>
                  <b-td>Default</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>

                <b-tr variant="primary">
                  <b-td>Primary</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>
                <b-tr variant="secondary">
                  <b-td>Secondary</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>
                <b-tr variant="success">
                  <b-td>Success</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>
                <b-tr variant="danger">
                  <b-td>Danger</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>
                <b-tr variant="warning">
                  <b-td>Warning</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>
                <b-tr variant="info">
                  <b-td>Info</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>
                <b-tr variant="light">
                  <b-td>Light</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>
                <b-tr variant="dark">
                  <b-td>Dark</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="striped" title="Striped Rows Table">
            <b-table-simple striped responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="striped" title="Striped Rows Table Dark">
            <b-table-simple striped dark responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="striped" title="Striped Rows Table Success">
            <b-table-simple variant="success" striped responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard title="Striped columns">
            <b-table-simple striped-columns responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard title="Striped columns Dark">
            <b-table-simple dark striped-columns responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard title="Striped columns Success">
            <b-table-simple variant="success" striped-columns responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="hoverable-row" title="Hoverable rows">
            <b-table-simple responsive hover class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="active" title="Active Tables">
            <b-table-simple responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th scope="col">#</b-th>
                  <b-th scope="col">First</b-th>
                  <b-th scope="col">Last</b-th>
                  <b-th scope="col">Handle</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr class="table-active">
                  <b-td>1</b-td>
                  <b-td>Mark</b-td>
                  <b-td>Otto</b-td>
                  <b-td>@mdo</b-td>
                </b-tr>
                <b-tr>
                  <b-td>2</b-td>
                  <b-td>Jacob</b-td>
                  <b-td>Thornton</b-td>
                  <b-td>@fat</b-td>
                </b-tr>
                <b-tr>
                  <b-td>3</b-td>
                  <b-td class="table-active">Larry the Bird</b-td>
                  <b-td>Simsons</b-td>
                  <b-td>@twitter</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard title="Active Tables Dark">
            <b-table-simple dark responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th scope="col">#</b-th>
                  <b-th scope="col">First</b-th>
                  <b-th scope="col">Last</b-th>
                  <b-th scope="col">Handle</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr class="table-active">
                  <b-td>1</b-td>
                  <b-td>Mark</b-td>
                  <b-td>Otto</b-td>
                  <b-td>@mdo</b-td>
                </b-tr>
                <b-tr>
                  <b-td>2</b-td>
                  <b-td>Jacob</b-td>
                  <b-td>Thornton</b-td>
                  <b-td>@fat</b-td>
                </b-tr>
                <b-tr>
                  <b-td>3</b-td>
                  <b-td class="table-active">Larry the Bird</b-td>
                  <b-td>Simsons</b-td>
                  <b-td>@twitter</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="bordered" title="Bordered Table">
            <b-table-simple responsive bordered class="mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="border-color" title="Bordered color Table">
            <b-table-simple responsive bordered border-variant="primary" class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="borderless" title="Tables without borders">
            <b-table-simple responsive borderless class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard title="Tables without borders Dark">
            <b-table-simple responsive dark borderless class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="small" title="Small tables">
            <b-table-simple responsive small class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="small" title="Small Tables Dark">
            <b-table-simple responsive dark small class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="dividers" title="Table group dividers">
            <b-table-simple responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody class="table-group-divider">
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="alignment" title="Vertical alignment">
            <b-table-simple responsive align="middle" class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th scope="col" class="w-25">Heading 1</b-th>
                  <b-th scope="col" class="w-25">Heading 2</b-th>
                  <b-th scope="col" class="w-25">Heading 3</b-th>
                  <b-th scope="col" class="w-25">Heading 4</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr>
                  <b-td>This cell inherits <code>align: middle;</code> from the table</b-td>
                  <b-td>This cell inherits <code>align: middle;</code> from the table</b-td>
                  <b-td>This cell inherits <code>align: middle;</code> from the table</b-td>
                  <b-td>This here is some placeholder text, intended to take up quite a bit of vertical space, to
                    demonstrate how the vertical alignment works in the preceding cells.
                  </b-td>
                </b-tr>
                <b-tr align="bottom">
                  <b-td>This cell inherits <code>align: bottom;</code> from the table row</b-td>
                  <b-td>This cell inherits <code>align: bottom;</code> from the table row</b-td>
                  <b-td>This cell inherits <code>align: bottom;</code> from the table row</b-td>
                  <b-td>This here is some placeholder text, intended to take up quite a bit of vertical space, to
                    demonstrate how the vertical alignment works in the preceding cells.
                  </b-td>
                </b-tr>
                <b-tr>
                  <b-td>This cell inherits <code>align: middle;</code> from the table</b-td>
                  <b-td>This cell inherits <code>align: middle;</code> from the table</b-td>
                  <b-td class="align-top">This cell is aligned to the top.</b-td>
                  <b-td>This here is some placeholder text, intended to take up quite a bit of vertical space, to
                    demonstrate how the vertical alignment works in the preceding cells.
                  </b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="nesting" title="Nesting Table">
            <b-table-simple responsive bordered striped class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th scope="col">#</b-th>
                  <b-th scope="col">First</b-th>
                  <b-th scope="col">Last</b-th>
                  <b-th scope="col">Handle</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr>
                  <b-td>1</b-td>
                  <b-td>Mark</b-td>
                  <b-td>Otto</b-td>
                  <b-td>@mdo</b-td>
                </b-tr>
                <b-tr>
                  <b-td colspan="4">
                    <b-table-simple class="mb-0">
                      <b-thead>
                        <b-tr>
                          <b-th scope="col">Header</b-th>
                          <b-th scope="col">Header</b-th>
                          <b-th scope="col">Header</b-th>
                        </b-tr>
                      </b-thead>
                      <b-tbody>
                        <b-tr>
                          <b-td>A</b-td>
                          <b-td>First</b-td>
                          <b-td>Last</b-td>
                        </b-tr>
                        <b-tr>
                          <b-td>B</b-td>
                          <b-td>First</b-td>
                          <b-td>Last</b-td>
                        </b-tr>
                        <b-tr>
                          <b-td>C</b-td>
                          <b-td>First</b-td>
                          <b-td>Last</b-td>
                        </b-tr>
                      </b-tbody>
                    </b-table-simple>
                  </b-td>
                </b-tr>
                <b-tr>
                  <b-td>3</b-td>
                  <b-td>Larry</b-td>
                  <b-td>the Bird</b-td>
                  <b-td>@twitter</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="head-option" title="Table head">
            <b-table-simple responsive class="table-centered mb-0">
              <b-thead variant="light">
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="tablehead" title="Table head Dark">
            <b-table-simple responsive class="table-centered mb-0">
              <b-thead variant="dark">
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="tablefoot" title="Table foot">
            <b-table-simple responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
              <b-tfoot>
                <b-tr>
                  <b-td v-for="(footer, idx) in tableData.foot" :key="idx">{{ footer }}</b-td>
                </b-tr>
              </b-tfoot>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="captions" title="Captions">
            <b-table-simple responsive class="table-centered mb-0">
              <caption>
                List of users
              </caption>
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="captions" title="Captions">
            <b-table-simple responsive class="table-centered mb-0" caption-top>
              <caption>
                List of users
              </caption>
              <b-thead>
                <b-tr>
                  <b-th v-for="(header, idx) in tableData.head" :key="idx" scope="col">{{ header }}</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr v-for="(item, idx) in tableData.body" :key="idx">
                  <b-td>{{ item.column1 }}</b-td>
                  <b-td>{{ item.column2 }}</b-td>
                  <b-td>{{ item.column3 }}</b-td>
                  <b-td>{{ item.column4 }}</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="responsive" title="Always responsive">
            <b-table-simple responsive class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th scope="col">#</b-th>
                  <b-th scope="col">Heading</b-th>
                  <b-th scope="col">Heading</b-th>
                  <b-th scope="col">Heading</b-th>
                  <b-th scope="col">Heading</b-th>
                  <b-th scope="col">Heading</b-th>
                  <b-th scope="col">Heading</b-th>
                  <b-th scope="col">Heading</b-th>
                  <b-th scope="col">Heading</b-th>
                  <b-th scope="col">Heading</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr>
                  <b-td>1</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>
                <b-tr>
                  <b-td>2</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>
                <b-tr>
                  <b-td>3</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                  <b-td>Cell</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="responsive" title="With avatars">
            <b-table-simple responsive hover class="table-centered mb-0">
              <b-thead variant="light">
                <b-tr>
                  <b-th scope="col">Name</b-th>
                  <b-th scope="col">Title</b-th>
                  <b-th scope="col">Email</b-th>
                  <b-th scope="col">Role</b-th>
                  <b-th scope="col">Action</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr>
                  <b-td>
                    <div class="d-flex align-items-center gap-1">
                      <img :src="avatar2" alt="" class="avatar-sm rounded-circle"/>
                      <div class="d-block">
                        <h5 class="mb-0">Tony M. Carter</h5>
                      </div>
                    </div>
                  </b-td>
                  <b-td>Designer</b-td>
                  <b-td>tonymcarter@jourrapide.com</b-td>
                  <b-td>Member</b-td>
                  <b-td><a href="#!" class="btn btn-primary btn-sm w-100">Edit</a></b-td>
                </b-tr>
                <b-tr>
                  <b-td>
                    <div class="d-flex align-items-center gap-1">
                      <img :src="avatar1" alt="" class="avatar-sm rounded-circle"/>
                      <div class="d-block">
                        <h5 class="mb-0">James E. Chamb</h5>
                      </div>
                    </div>
                  </b-td>
                  <b-td>UI/UX Designer</b-td>
                  <b-td>jamesechambliss@teleworm.us</b-td>
                  <b-td>Admin</b-td>
                  <b-td><a href="#!" class="btn btn-primary btn-sm w-100">Edit</a></b-td>
                </b-tr>
                <b-tr>
                  <b-td>
                    <div class="d-flex align-items-center gap-1">
                      <img :src="avatar4" alt="" class="avatar-sm rounded-circle"/>
                      <div class="d-block">
                        <h5 class="mb-0">Charlotte J. Torres</h5>
                      </div>
                    </div>
                  </b-td>
                  <b-td>Copywriter</b-td>
                  <b-td>charlotte@jourrapide.com</b-td>
                  <b-td>Member</b-td>
                  <b-td><a href="#!" class="btn btn-primary btn-sm w-100">Edit</a></b-td>
                </b-tr>
                <tr class="table-active">
                  <b-td>
                    <div class="d-flex align-items-center gap-1">
                      <img :src="avatar6" alt="" class="avatar-sm rounded-circle"/>
                      <div class="d-block">
                        <h5 class="mb-0 d-flex align-items-center gap-1">Mary J. Germain<i
                            class="bx bxs-badge-check text-success"></i></h5>
                      </div>
                    </div>
                  </b-td>
                  <b-td>Full Stack</b-td>
                  <b-td>maryjgermain@jourrapide.com</b-td>
                  <b-td>CEO</b-td>
                  <b-td><a href="#!" class="btn btn-primary btn-sm w-100">Edit</a></b-td>
                </tr>
                <b-tr>
                  <b-td>
                    <div class="d-flex align-items-center gap-1">
                      <img :src="avatar7" alt="" class="avatar-sm rounded-circle"/>
                      <div class="d-block">
                        <h5 class="mb-0">Kevin C. Reyes</h5>
                      </div>
                    </div>
                  </b-td>
                  <b-td>Director of Product</b-td>
                  <b-td>kevincreyes@jourrapide.com</b-td>
                  <b-td>Member</b-td>
                  <b-td><a href="#!" class="btn btn-primary btn-sm w-100">Edit</a></b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="responsive" title="With checkboxes">
            <b-table-simple responsive striped borderless class="table-centered mb-0">
              <b-thead variant="light">
                <b-tr>
                  <b-th scope="col">
                    <div class="form-check">
                      <b-form-checkbox id="flexCheckDefault5"/>
                    </div>
                  </b-th>
                  <b-th scope="col">Name</b-th>
                  <b-th scope="col">Title</b-th>
                  <b-th scope="col">Email</b-th>
                  <b-th scope="col">Role</b-th>
                  <b-th scope="col">Action</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr>
                  <b-td>
                    <div class="form-check">
                      <b-form-checkbox id="flexCheckDefault"/>
                    </div>
                  </b-td>
                  <b-td> Tony M. Carter</b-td>
                  <b-td>Designer</b-td>
                  <b-td>tonymcarter@jourrapide.com</b-td>
                  <b-td>Member</b-td>
                  <b-td><a href="#!" class="btn btn-primary btn-sm w-100">Edit</a></b-td>
                </b-tr>
                <b-tr>
                  <b-td>
                    <div class="form-check">
                      <b-form-checkbox id="flexCheckDefault2"/>
                    </div>
                  </b-td>
                  <b-td>James E. Chamb</b-td>
                  <b-td>UI/UX Designer</b-td>
                  <b-td>jamesechambliss@teleworm.us</b-td>
                  <b-td>Admin</b-td>
                  <b-td><a href="#!" class="btn btn-primary btn-sm w-100">Edit</a></b-td>
                </b-tr>
                <b-tr>
                  <b-td>
                    <div class="form-check">
                      <b-form-checkbox id="flexCheckDefault3"/>
                    </div>
                  </b-td>
                  <b-td> Charlotte J. Torres</b-td>
                  <b-td>Copywriter</b-td>
                  <b-td>charlotte@jourrapide.com</b-td>
                  <b-td>Member</b-td>
                  <b-td><a href="#!" class="btn btn-primary btn-sm w-100">Edit</a></b-td>
                </b-tr>
                <b-tr>
                  <b-td>
                    <div class="form-check">
                      <b-form-checkbox id="flexCheckDefault4"/>
                    </div>
                  </b-td>
                  <b-td> Mary J. Germain <i class="bx bxs-badge-check text-success"></i></b-td>
                  <b-td>Full Stack</b-td>
                  <b-td>maryjgermain@jourrapide.com</b-td>
                  <b-td>CEO</b-td>
                  <b-td><a href="#!" class="btn btn-primary btn-sm w-100">Edit</a></b-td>
                </b-tr>
                <b-tr>
                  <b-td>
                    <div class="form-check">
                      <b-form-checkbox id="flexCheckDefault5"/>
                    </div>
                  </b-td>
                  <b-td>Kevin C. Reyes</b-td>
                  <b-td>Director of Product</b-td>
                  <b-td>kevincreyes@jourrapide.com</b-td>
                  <b-td>Member</b-td>
                  <b-td><a href="#!" class="btn btn-primary btn-sm w-100">Edit</a></b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>

          <UIComponentCard id="nesting1" title="Nesting Table">
            <b-table-simple responsive striped bordered class="table-centered mb-0">
              <b-thead>
                <b-tr>
                  <b-th scope="col">Invoice Number</b-th>
                  <b-th scope="col">Invoice Amount</b-th>
                  <b-th scope="col">Confirmation by the client</b-th>
                  <b-th scope="col">Planned payment date</b-th>
                </b-tr>
              </b-thead>
              <b-tbody>
                <b-tr>
                  <b-td>F-011221/21</b-td>
                  <b-td>{{currency}} 879.500</b-td>
                  <b-td>11/05/2023</b-td>
                  <b-td>12/05/2023</b-td>
                </b-tr>
                <b-tr>
                  <b-td colspan="4">
                    <b-table-simple class="mb-0">
                      <b-thead>
                        <b-tr>
                          <b-th scope="col">ERP number</b-th>
                          <b-th scope="col">Carrier legal entity</b-th>
                          <b-th scope="col">Responsible logistician</b-th>
                          <b-th scope="col">Status</b-th>
                        </b-tr>
                      </b-thead>
                      <b-tbody>
                        <b-tr>
                          <b-td>3-128-3</b-td>
                          <b-td>ToBrookfield Asset Management</b-td>
                          <b-td>
                            <div class="d-flex align-items-center gap-1">
                              <img :src="avatar7" alt="" class="avatar-sm rounded-circle"/>
                              <div class="d-block">
                                <h5 class="mb-0">Kevin C. Reyes</h5>
                              </div>
                            </div>
                          </b-td>
                          <b-td>
                            <b-badge :variant="null" class="bg-success-subtle text-success py-1 px-2">Verified</b-badge>
                          </b-td>
                        </b-tr>
                        <b-tr>
                          <b-td>3-128-2</b-td>
                          <b-td>Brookfield Asset Management</b-td>
                          <b-td>
                            <div class="d-flex align-items-center gap-1">
                              <img :src="avatar6" alt="" class="avatar-sm rounded-circle"/>
                              <div class="d-block">
                                <h5 class="mb-0">Mary J. Germain</h5>
                              </div>
                            </div>
                          </b-td>
                          <b-td>
                            <b-badge :variant="null" class="bg-warning-subtle text-warning py-1 px-2">Pending</b-badge>
                          </b-td>
                        </b-tr>
                        <b-tr>
                          <b-td>3-128-1</b-td>
                          <b-td>Westfield Asset Management</b-td>
                          <b-td>
                            <div class="d-flex align-items-center gap-1">
                              <img :src="avatar8" alt="" class="avatar-sm rounded-circle"/>
                              <div class="d-block">
                                <h5 class="mb-0">Charlotte J. Torres</h5>
                              </div>
                            </div>
                          </b-td>
                          <b-td>
                            <b-badge :variant="null" class="bg-danger-subtle text-danger py-1 px-2">Rejected</b-badge>
                          </b-td>
                        </b-tr>
                      </b-tbody>
                    </b-table-simple>
                  </b-td>
                </b-tr>
                <b-tr>
                  <b-td>F-011221/19</b-td>
                  <b-td>{{currency}} 93.250</b-td>
                  <b-td>9/05/2023</b-td>
                  <b-td>10/05/2023</b-td>
                </b-tr>
              </b-tbody>
            </b-table-simple>
          </UIComponentCard>
        </b-col>

        <b-col xl="3">
          <AnchorNavigation :elements="anchorNavigation"/>
        </b-col>
      </b-row>
  </VerticalLayout>
</template>

<script setup lang="ts">
import VerticalLayout from "@/layouts/VerticalLayout.vue";
import UIComponentCard from '@/components/UIComponentCard.vue'
import AnchorNavigation from '@/components/AnchorNavigation.vue'
import { currency } from "@/helpers/constants";

import avatar1 from '@/assets/images/users/avatar-1.jpg'
import avatar2 from '@/assets/images/users/avatar-2.jpg'
import avatar4 from '@/assets/images/users/avatar-4.jpg'
import avatar6 from '@/assets/images/users/avatar-6.jpg'
import avatar7 from '@/assets/images/users/avatar-7.jpg'
import avatar8 from '@/assets/images/users/avatar-8.jpg'

const tableData = {
  head: ['#', 'First', 'Last', 'Handle'],
  body: [
    {
      column1: 1,
      column2: 'Mark',
      column3: 'Otto',
      column4: '@mdo'
    },
    {
      column1: 2,
      column2: 'Jacob',
      column3: 'Thornton',
      column4: '@fat'
    },
    {
      column1: 3,
      column2: 'Larry the Bird',
      column3: 'Simsons',
      column4: '@twitter'
    }
  ],
  foot: ['Footer', 'Footer', 'Footer', 'Footer']
}

const anchorNavigation = [
  {
    id: 'basic',
    title: 'Basic Example'
  },
  {
    id: 'inverse',
    title: 'Inverse Table'
  },
  {
    id: 'striped',
    title: 'Striped Rows Table'
  },
  {
    id: 'hoverable-row',
    title: 'Hoverable rows'
  },
  {
    id: 'active',
    title: 'Active Table'
  },
  {
    id: 'bordered',
    title: 'Bordered Table'
  },
  {
    id: 'border-color',
    title: 'Bordered Color Table'
  },
  {
    id: 'borderless',
    title: 'Basic Borderless Table'
  },
  {
    id: 'small',
    title: 'Small Table'
  },
  {
    id: 'alignment',
    title: 'Alignment Table'
  },
  {
    id: 'nesting',
    title: 'Nesting Table'
  },
  {
    id: 'head-option',
    title: 'Table head options Table'
  },
  {
    id: 'tablefoot',
    title: 'Tablefoot'
  },
  {
    id: 'captions',
    title: 'Captions'
  },
  {
    id: 'responsive',
    title: 'Always Responsive Table'
  }
]
</script>
