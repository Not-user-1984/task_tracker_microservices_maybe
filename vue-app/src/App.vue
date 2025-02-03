<template>
  <div id="app">
    <TokenForm />
  </div>
</template>

<script>
import TokenForm from './components/TokenForm.vue';

export default {
  components: {
    TokenForm
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>