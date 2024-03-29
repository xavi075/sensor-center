import { useState, useEffect } from 'react';
import LastInfo from "../data/components/LastInfo"
import './HomePage.css'
import { getLastMeasure, getLastWaterInfo, getUserProfile } from "../../utils/api";
import { ILastInfo, IData, IProfile } from '../../utils/interfaces';
import { useUser } from '../../context/UserContext';
import LastMeasure from './components/LastMeasure';

export function HomePage() {
  const { usernameId } = useUser();
  const [UserInfo, setUserInfo] = useState<IProfile>();
  const [UserMeasures, setUserMeasures] = useState<IData>();
  const [lastInfo, setLastInfo] = useState<ILastInfo>();

  useEffect(() => {
    if (usernameId != null){
      getUserProfile(usernameId)
      .then((response) => {
        setUserInfo(response);
        getLastMeasure(usernameId)
        .then((response) => {
          setUserMeasures(response)
          getLastWaterInfo(usernameId)
          .then((response) => {
              setLastInfo(response)
          })
          .catch((error) => {
              console.error('Error when Lat Water info: ', error);
          });
        })
        .catch((error) => {
          console.error('Error when user devices: ', error);
        });
      })
      .catch((error) => {
        console.error('Error when user devices: ', error);
      });
    }
  }, [usernameId])

  return (
    <>           
    <div className="page-box home">
      <div className="column">
        <h3 className='welcome-message'>Benvingut/da, {UserInfo?.dades[0].nomUsuari}!</h3>
        <h2>Últimes mesures</h2>
        {UserMeasures?.dades.length === 0 ? <p>No hi ha mesures recents</p>:
         UserMeasures?.dades.map((mesura) => (
          <LastMeasure key={mesura.idDispositiu} nomDispositiu={mesura.nomDispositiu} dadaHum={mesura.dadaHum} dadaTemp={mesura.dadaTemp} dataHora={mesura.dataHora}/>
        ))}
      </div>
      <div className="column">
      <div className='spacing'></div>
      <h2>Últims regs</h2>
      {lastInfo?.dades[0].nomDispositiu === "" ?<p>No hi ha dades de reg a mostrar</p> :
        lastInfo?.dades.map((reg) => (
        <LastInfo key={reg.idDispositiu} deviceName={reg.nomDispositiu} finalData={reg.dataHoraFi} startingData={reg.dataHoraInici}/>
          ))
      }
      </div>
    </div>
    </>

  )
}