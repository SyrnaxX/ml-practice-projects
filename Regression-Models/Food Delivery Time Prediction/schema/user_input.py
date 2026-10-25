from pydantic import BaseModel ,field_validator,computed_field,Field
from typing import Annotated,Literal
import json
from datetime import datetime
class userInput(BaseModel):
    # ....schema...
    Distance : Annotated[float,Field(...,description='Enter distance in km',examples=[12.3,5.6])]
    No_of_signals : Annotated[int,Field(...,description='Enter numbetr of signals.',examples=[1,3,5])]
    Rider_Rating : Annotated[int,Field(...,description='Enter rider rating',examples=[4.5,3.2])]
    Cuisine_Type : Annotated[Literal['Pizza','Desserts','Biryani','Burger','South Indian','Bakery',
                                     'North Indian','Cafe','Chinese'],Field(...,description=('Enter Cusine type')
                                    ,examples=['North Indian','Biryani','Bakery'])]
    Traffic_Level: Annotated[Literal['Moderate', 'Low', 'High', 'Severe'],Field(...,
                                    description='Traffic level',examples=['High','Low','Severe'])]
    Weekend : Annotated[bool,Field(...,description='is Weekend',examples=['True','False'])]
    Festival :Annotated[bool,Field(...,description='is festival',examples=['True','False'])]
    Order_Items : Annotated[int,Field(...,description='No of order items',examples=[1,2])]
    Order_Hour : Annotated[str,Field(...,description='Time of order',examples=["2:45 PM","8:09 PM","11:11 AM"])]
    Weather : Annotated[Literal['Clear', 'Rain', 'Cloudy', 'Storm', 'Fog'],
                        Field(...,description='Enter wheather type',examples=['Clear','Cloudy','Storm'])]
    Pickup_Zone : Annotated[Literal['CBD', 'Residential', 'Industrial', 'Commercial', 'Suburban'],
                            Field(...,description="Pickup Zone",examples=['Residential','Industrial','Suburban'])]
    Dropoff_Zone : Annotated[Literal['Commercial', 'CBD', 'Residential', 'Industrial', 'Suburban'],
                             Field(...,description="Dropoff Zone",examples=['Commercial','Residential'])]
    Vehicle_Type : Annotated[Literal['Scooter', 'Bike', 'Electric Scooter', 'Bicycle'],
                             Field(...,description='Enter Vehicle_Type',examples=['Bike','Electric Scooter'])]
    ## computed field...
    @computed_field
    @property
    def Delivery_Distance_Category(self) -> str:
        if self.distance < 2:
            return "Short"
        elif self.distance < 7:
            return 'Medium'
        return 'Long'
    @computed_field
    @property
    def Time_period(self)-> str: 
        time_obj = datetime.strptime(self.Order_hour,"%I:%M%p") # ex:  2:45 PM
        hour = time_obj.hour
        # convert to Time_period
        if 6<= hour <12:
            return 'Morning'
        elif 12 <= hour < 16:
            return 'Afternoon'
        elif 16 <= hour<21:
            return 'Evening'
        return 'Night'