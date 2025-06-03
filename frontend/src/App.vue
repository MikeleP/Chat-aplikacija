<template>
  <div style="padding: 20px; font-family: monospace">
    <h3>Welcome to Chat Room</h3>

    <div v-if="!connected">
      <input v-model="username" placeholder="Enter username" />
      <button @click="connect">Connect</button>
    </div>

    <div v-else>
      <div class="messages">
        <div v-for="(msg, index) in messages" :key="index">
          <span v-html="msg"></span>
        </div>
      </div>

      <div style="margin-top: 20px">
        <input
          v-model="newMessage"
          @keyup.enter="sendMessage"
          placeholder="Type a message"
        />
        <button @click="sendMessage">Send</button>
      </div>
    </div>
  </div>
</template>
