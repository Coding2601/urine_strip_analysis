<template>
  <div>
    <h1>Upload Urine Strip Image</h1>
    <input type="file" @change="onFileChange" />
    <button @click="uploadImage">Upload</button>
    <div v-if="colors">
      <h2>Detected Colors:</h2>
      <ul>
        {{colors}}
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data () {
    return {
      file: null,
      colors: null
    }
  },
  methods: {
    onFileChange (event) {
      this.file = event.target.files[0]
    },
    async uploadImage () {
      if (!this.file) {
        alert('Please select an image file first!')
        return
      }
      const formData = new FormData()
      formData.append('image', this.file)

      try {
        const response = await fetch('http://localhost:8000/api/upload/', {
          method: 'POST',
          body: formData
        },
        {
          withCredentials: true
        })
        const result = await response.json()
        this.colors = result.colors
      } catch (error) {
        console.error('Error uploading image:', error)
      }
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}

li{
  list-style-type: none;
  margin: 0;
  padding: 0;
}
</style>
