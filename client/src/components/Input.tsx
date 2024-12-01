import { useEffect, useState } from "react";
import "./input.css"
import axios from "axios";

function Input() {
  const [locations,setLocations] = useState<string[]>([])
  const [location,setLocation] = useState<string>("")
  const [sqft,setSqft] = useState<string>("")
  const [bath,setBath] = useState<string>("")
  const [bhk,setBhk] = useState<string>("")
  const [price,setPrice] = useState<number>(0)
  useEffect(()=>{
      (async () => {
          try {
            const res = await axios.get("http://127.0.0.1:8001/api/location_names")
            setLocations(res.data.location)
          } catch (error) {
            console.log(error)
          }
      })()
  },[])

  const handleSubmit =async (e:React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await axios.post("http://127.0.0.1:8001/api/predict-price",{location:location,sqft:sqft,bath:bath,bhk:bath})
      setPrice(res.data)
    } catch (error) {
      console.log(error)
    }
  }
  return (
    <div>
      <h1>Predict Your House Price</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Sqft: </label>
          <input 
          type="text" 
          placeholder="Enter total square feet"
          value={sqft}
          onChange={(e)=>setSqft(e.target.value)}
          
          />
        </div>

        
        <div>
          <label>Bath: </label>
          <input type="text" placeholder="Enter No. of bathroom" 
          value={bath} onChange={(e)=>setBath(e.target.value)}/>
        </div>

        
        <div>
          <label>BHK: </label>
          <input type="text" placeholder="Enter BKH"  
          value={bhk}
          onChange={(e)=>setBhk(e.target.value)}/>
        </div>

        <div>
          <label>Gender: </label>
          <select value={location} onChange={(e)=>setLocation(e.target.value)}>
            <option value="">Select Location</option>
            {
              locations.map((location,index)=>(
                <option key={index} value={location}>{location}</option>
              ))
            }
          </select>
        </div>

        {/* Submit Button */}
        <div>
          <button type="submit">Submit</button>
        </div>
      </form>
      
      <h1>{price} Lakhs</h1>
    </div>
  );
}

export default Input;
