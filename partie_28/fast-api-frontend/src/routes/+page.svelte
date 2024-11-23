<script>
async function getData(){
const res = await fetch("http://localhost:8000/blah")
const data = await res.json()
if (res.ok) {
return data
} else {
throw new Error(data)
}
}
let promise = getData()
const handleClick = () => {
promise = getData()
}
</script>

<h1>Welcome to your library project</h1>
<p>Create your package using @sveltejs/package and preview/showcase your work with SvelteKit</p>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>
<button on:click={handleClick}>
Get Data
</button>
{#await promise}
<p>...Waiting</p>
{:then data}
<p>Data is {data.hello}</p>
{:catch error}
<p> Error is {error} </p>
{/await}
