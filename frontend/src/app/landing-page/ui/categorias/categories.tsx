
export default function LandingPageCategories () {

    return(
        <div className="grid grid-cols-3">
            <div className="flex justify-center items-center border border-black h-80 bg-neutral-400 cursor-pointer">
                <h1 className="text-white text-4xl drop-shadow-lg">Pantalones</h1> 
            </div>
            <div className="flex justify-center items-center border border-black h-80 bg-neutral-400 cursor-pointer">
                <h1 className="text-white text-4xl drop-shadow-lg">Poleras</h1>
            </div>
            <div className="flex justify-center items-center border border-black h-80 bg-neutral-400 cursor-pointer">
                <h1 className="text-white text-4xl drop-shadow-lg">Calzado</h1>
            </div>
        </div>
    )
}