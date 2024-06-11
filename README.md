# swollen
BeeSafe: Comprehensive Risk Assessment for Bee Conservation

https://pypi.org/user/fedirek/


Bee Score: Enhancing Pollination, Sustaining Life
Awareness of Bee score can increase pollination by 30%
Don’t wait get your score

## Architecture
### Data flow

```mermaid
  flowchart TB
    subgraph git-repo
      ml-model
      flask
    end
    subgraph azure
    web-app
    end
    subgraph pip
    swollen-package
    end
    subgraph open-source
    swollen
    end
    swollen --> swollen-package
    web-app --- web-page
    flask -.-> ml-model
    flask -.-> swollen-package
    web-app --> git-repo
```

### QA

* MR to main from uat
* test in local first

## User navigation
```mermaid
  flowchart LR
      A["User provide input"] --> B["Output of the model"] --> C["Web-page shows how user can help environment"]
```
