import { useEffect, useState } from "react";
import NewPlantForm from "./NewPlantForm";
import PlantList from "./PlantList";
import Search from "./Search";

function PlantPage() {
  const [plants, setPlants] = useState([
    {
      id: 0,
      name: "",
      image: "",
      price: 0,
      is_in_stock: false,
    },
  ]);
  const [searchTerm, setSearchTerm] = useState("");

  useEffect(() => {
    fetch("/plants")
      .then((r) => r.json())
      .then((plantsArray) => {
        setPlants(plantsArray);
      });
  }, []);

  const handleAddPlant = (newPlant) => {
    const updatedPlantsArray = [...plants, newPlant];
    setPlants(updatedPlantsArray);
  };


  const handleUpdatePlant = (updatedPlant) => {
    if (!updatedPlant || !updatedPlant.id) {
      console.error("Invalid updated plant object or missing id");
      return;
    }

    const updatedPlantsArray = plants.map((plant) => {

      const updatedPlant = {
        "id": plants.id,
        "name": updatedPlant.name,
        "image": updatedPlant.image,
        "price": updatedPlant.price,
        "is_in_stock": updatedPlant.is_in_stock,
        
      };
      if (plant.id === updatedPlant.id) {
        return { ...plants, ...updatedPlant };
      } else {
        return plant;
      }
    });
    setPlants(updatedPlantsArray);
  };

  const handleDeletePlant = (id) => {
    const updatedPlantsArray = plants.filter((plant) => plant.id !== id);
    setPlants(updatedPlantsArray);
  };

  const displayedPlants = plants.filter((plant) => {
    return plant.name.toLowerCase().includes(searchTerm.toLowerCase());
  });

  return (
    <main>
      <NewPlantForm onAddPlant={handleAddPlant} />
      <Search searchTerm={searchTerm} onSearchChange={setSearchTerm} />
      <PlantList
        plants={displayedPlants}
        handleUpdatePlant={handleUpdatePlant}
        handleDeletePlant={handleDeletePlant}
      />
    </main>
  );
}

export default PlantPage;
