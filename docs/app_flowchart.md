flowchart TD
    Homepage[Homepage: Navigation to Teams, Players, Games] --> Teams[Teams Listing with Search/Filter]
    Homepage --> Players[Players Listing with Search/Filter]
    Homepage --> Games[Games Listing with Search/Filter]
    Teams --> TeamDetail[Team Detail Page]
    Players --> PlayerDetail[Player Detail Page]
    Games --> GameDetail[Game Detail Page]
    
    subgraph Deployment
        Container[Containerized Flask & SQLite Application]
    end
    
    TeamDetail --> Container
    PlayerDetail --> Container
    GameDetail --> Container