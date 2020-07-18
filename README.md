primenumbertweet
========
 ... is now tweeting on [@sosuubot](https://twitter.com/sosuubot)!

## What is this?

It is a bot working on Google App Engine which tweets a prime number per hour.

## Deploy

### Requirements

- Google Cloud SDK

### Setting secrets to `secret.yaml`

```yaml
env_variables:
  API_KEY: "XXXXXXXXXXXXX"
  API_SECRET: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  ACCESS_TOKEN_KEY: "XXXXXXXXXXXXX"
  ACCESS_TOKEN_SECRET: "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
  DEBUG_TOKEN: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
```

### Let's deploy

```
$ make deploy
```
