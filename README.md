# swollen
BeeSafe: Comprehensive Risk Assessment for Bee Conservation


Bee Score: Enhancing Pollination, Sustaining Life
Awareness of Bee score can increase pollination by 30%
Don’t wait get your score

## Architecture
### Data flow

```mermaid
  flowchart TB
    subgraph git-repo
      subgraph back-end
      ml-model
      end
      subgraph front-end
      flask
      end
    end
    subgraph azure
    web-app
    end
    web-app --- web-page
    flask -.-> ml-model
    web-app --> git-repo 
```

### QA

* MR to main from uat
* test in local first
