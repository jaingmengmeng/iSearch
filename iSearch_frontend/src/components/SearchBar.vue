<template>
  <div class="search-bar">
    <Dropdown
      trigger="custom"
      :visible="visible"
      class="search-dropdown"
      placement="bottom"
    >
      <Input
        class="search-input"
        v-model="query"
        size="large"
        placeholder="输入关键词，在 iSearch 上搜索"
        icon="ios-search"
        :maxlength="100"
        @on-change="showDropdown"
        @on-focus="showDropdown"
        @on-click="submitSearch"
        @on-enter="submitSearch"
        @on-blur="hideDropDown"
      ></Input>
      <Dropdown-menu
        class="search-dropdown-menu"
        slot="list"
        v-for="(item, i) in dropdown_list.slice(0, max_dropdown)"
        :key="i"
      >
        <div class="search-dropdown-item" @click="selectDropdown(item)">
          {{ item }}
        </div>
      </Dropdown-menu>
    </Dropdown>
    <!-- <AutoComplete
      v-model="query"
      icon="ios-search"
      :data="dropdown_list.slice(0, max_dropdown)"
      @on-search="getAutoComplete"
      placeholder="input here"
      style="width:100%"
    ></AutoComplete> -->
  </div>
</template>

<script>
export default {
  name: 'SearchBar',
  props: ['q'],
  data() {
    return {
      query: '',
      max_dropdown: 7,
      visible: false,
      dropdown_list: []
    };
  },
  created: function() {
    if (this.q !== '') {
      this.query = this.q;
    }
  },
  methods: {
    async getAutoComplete() {
      await this.$axios
        .get('/api/autocomplete/', {
          params: {
            q: this.query
          }
        })
        .then(res => {
          this.dropdown_list = res.data;
        })
        .catch(function(error) {
          console.log(error);
        });
    },
    async showDropdown() {
      if (this.query === '') {
        this.visible = false;
        this.dropdown_list = [];
      } else {
        await this.getAutoComplete();
        if (this.dropdown_list.length === 0) {
          this.visible = false;
        } else {
          this.visible = true;
        }
      }
    },
    hideDropDown() {
      this.visible = false;
    },
    selectDropdown(item) {
      this.query = item;
      this.submitSearch();
    },
    submitSearch() {
      this.visible = false;
      if (this.query === '') {
        this.$Message.warning('请输入搜索词');
      } else {
        this.$emit('query', this.query);
      }
    }
  }
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped lang="scss">
.search-bar {
  // display: inline;
  // max-width: 560px;
  width: 100%;
  .search-dropdown {
    // max-width: 560px;
    width: 100%;
    .search-input {
      // max-width: 560px;
      width: 100%;
    }
    .search-input :nth-last-child(1) {
      font-size: 18px;
      height: 45px;
      line-height: 40px;
    }
    .search-input :nth-last-child(2) {
      font-size: 18px;
      height: 45px;
      line-height: 45px;
      cursor: pointer;
    }
    .search-dropdown-menu {
      // max-width: 560px;
      width: 100%;
      .search-dropdown-item {
        // max-width: 560px;
        cursor: pointer;
        width: 100%;
        font-size: 18px;
        text-align: left;
        padding-left: 10px;
        padding-right: 10px;
        height: 45px;
        line-height: 40px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      .search-dropdown-item:hover {
        background-color: #ecf0f1;
      }
    }
  }
}
</style>
