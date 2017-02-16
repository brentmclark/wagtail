## How to create and launch virtual environment

`virtualenv -p /usr/local/bin/python3.6 venv`

then

`source venv/bin/activate`

## `GraphQL` and `GraphiQL`

Graphql and Graphiql are available at /api/graphql and /api/graphiql respectively

#### GraphiQL

`Graphiql` is a very handy tool for testing and troubleshooting `GraphQL`.

Try this query for example:

```javascript
query articles {
  articles {
    id
    title
    date
    intro
    body
  }
}
```